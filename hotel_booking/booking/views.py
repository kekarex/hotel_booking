import os
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.views import redirect_to_login
from django.db.models import Count, Q, F
from .models import Room, Booking
from .forms import BookingForm
from django.conf import settings

'''CATEGORY_DESCRIPTIONS = {
    'Standard': 'Комфортный стандартный номер для недорогого проживания.',
    'Suite':    'Роскошный сьют с отдельной гостиной и кухней.',
    'Family':   'Большой семейный номер с дополнительными кроватями.',
    'Business': 'Уютный бизнес-класс с рабочим местом и полным набором услуг.',
    'Deluxe':   'Просторный номер Делюкс с панорамным видом и VIP-сервисом.'
}'''


CATEGORY_DESCRIPTIONS = {
    'Business': 'Уютный бизнес-класс с рабочим местом и полным набором услуг.',
    'Deluxe':   'Просторный номер Делюкс с панорамным видом и VIP-сервисом.',
    'Standard': 'Комфортный стандартный номер для недорогого проживания.',
    'Suite':    'Роскошный сьют с отдельной гостиной и кухней.',
    'Family':   'Большой семейный номер с дополнительными кроватями.'
}

app_name = 'booking'

def category_list(request):
    # получаем даты заезда/выезда или дефолт
    check_in  = request.GET.get('check_in')  or date.today().isoformat()
    check_out = request.GET.get('check_out') or (date.today() + timedelta(days=1)).isoformat()

    # подсчёт общее/забронировано
    qs = (
        Room.objects.values('kind')
        .annotate(
            total=Count('id'),
            booked=Count(
                'booking',
                filter=Q(
                    booking__check_in__lt=check_out,
                    booking__check_out__gt=check_in
                )
            )
        )
        .annotate(available=F('total') - F('booked'))
    )

    categories = []
    for c in qs:
        kind = c['kind']
        # загружаем статические картинки для категории
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'categories', kind.lower())
        images = []
        if os.path.isdir(static_dir):
            for fn in sorted(os.listdir(static_dir)):
                if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    images.append(settings.STATIC_URL + f'images/categories/{kind.lower()}/{fn}')

        # берём первую комнату для примера параметров
        sample = Room.objects.filter(kind=kind).first()

        categories.append({
            'kind':         kind,
            'total':        c['total'],
            'available':    c['available'],
            'description':  CATEGORY_DESCRIPTIONS.get(kind, ''),
            'area':         sample.area if sample else '',
            'bed_type':     sample.bed_type if sample else '',
            'parking':      sample.parking if sample else '',
            'tv':           sample.tv if sample else '',
            'air_conditioning': sample.air_conditioning if sample else '',
            'wifi':         sample.wifi if sample else '',
            'iron':         sample.iron if sample else '',
            'images':       images,
            'url':          reverse('booking:rooms_by_category', args=[kind])
                                + f'?check_in={check_in}&check_out={check_out}'
        })

    # нужный порядок вывода
    ORDER = ['Standard', 'Family', 'Suite', 'Business', 'Deluxe']
    categories.sort(key=lambda x: ORDER.index(x['kind']) if x['kind'] in ORDER else len(ORDER))

    return render(request, 'booking/category_list.html', {
        'categories': categories,
        'check_in':   check_in,
        'check_out':  check_out,
    })


def rooms_by_category(request, kind):
    check_in  = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    rooms_qs = Room.objects.filter(kind=kind)
    if check_in and check_out:
        rooms_qs = rooms_qs.exclude(
            booking__check_in__lt=check_out,
            booking__check_out__gt=check_in
        )

    rooms = []
    for room in rooms_qs:
        media_folder = os.path.join(settings.MEDIA_ROOT, 'rooms', str(room.number))
        imgs = []
        if os.path.isdir(media_folder):
            for fn in sorted(os.listdir(media_folder)):
                if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    imgs.append(settings.MEDIA_URL + f'rooms/{room.number}/{fn}')
        rooms.append({'room': room, 'images': imgs})

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
