from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.views import redirect_to_login
from django.db.models import Count, Q, F
from .models import Room, Booking
from .forms import BookingForm

def category_list(request):
    # даты
    check_in  = request.GET.get('check_in')  or date.today().isoformat()
    check_out = request.GET.get('check_out') or (date.today()+timedelta(days=1)).isoformat()

    # агрегируем: всего/забронировано/свободно по каждой категории
    qs = Room.objects.values('kind') \
        .annotate(total=Count('id'),
                  booked=Count('booking',
                               filter=Q(booking__check_in__lt=check_out,
                                        booking__check_out__gt=check_in))) \
        .annotate(available=F('total') - F('booked'))

    categories = []
    for c in qs:
        categories.append({
            'kind':      c['kind'],
            'total':     c['total'],
            'available': c['available'],
            'url':       f"{ reverse('booking:rooms_by_category', args=[c['kind']]) }?check_in={check_in}&check_out={check_out}"
        })

    return render(request, 'booking/category_list.html', {
        'categories': categories,
        'check_in':   check_in,
        'check_out':  check_out,
    })

def rooms_by_category(request, kind):
    # даты
    check_in  = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    # фильтруем комнаты
    rooms = Room.objects.filter(kind=kind)
    if check_in and check_out:
        rooms = rooms.exclude(
            booking__check_in__lt=check_out,
            booking__check_out__gt=check_in
        )

    return render(request, 'booking/rooms_by_category.html', {
        'kind':      kind,
        'rooms':     rooms,
        'check_in':  check_in,
        'check_out': check_out,
    })

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    check_in  = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        form = BookingForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            b.user = request.user
            b.room = room
            b.save()
            return redirect('booking:rooms_by_category', kind=room.kind)
    else:
        form = BookingForm(initial={'check_in': check_in, 'check_out': check_out})

    return render(request, 'booking/room_detail.html', {
        'room':      room,
        'form':      form,
        'check_in':  check_in,
        'check_out': check_out,
    })
