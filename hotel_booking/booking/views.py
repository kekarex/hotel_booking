from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from .models import Room, Booking
from .forms import BookingForm

# Список категорий
def category_list(request):
    categories = Room.objects.values_list('kind', flat=True).distinct()
    return render(request, 'booking/category_list.html', {'categories': categories})

# Список номеров по категории с фильтром дат
def rooms_by_category(request, kind):
    rooms = Room.objects.filter(kind=kind)
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    available_rooms = rooms
    # если указаны даты, исключаем занятые
    if check_in and check_out:
        available_rooms = rooms.exclude(
            booking__check_in__lt=check_out,
            booking__check_out__gt=check_in
        )
    return render(request, 'booking/rooms_by_category.html', {
        'kind': kind,
        'rooms': available_rooms,
        'check_in': check_in,
        'check_out': check_out,
    })

# Детали номера и бронирование
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            try:
                booking.save()
                messages.success(request, 'Номер успешно забронирован!')
                return redirect('booking:category_list')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = BookingForm()
    return render(request, 'booking/room_detail.html', {
        'room': room,
        'form': form,
    })