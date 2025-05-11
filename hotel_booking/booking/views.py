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
    'Family':   'Большой семейный номер с дополнительными кроватями.',
}


CATEGORY_DESCRIPTIONS = {
    'Standard': 'Комфортный стандартный номер для недорогого проживания.',
    'Family':   'Просторный семейный номер с дополнительными кроватями.',
    'Suite':    'Роскошный сьют с отдельной гостиной и кухней.',
    'Business': 'Уютный бизнес-класс с рабочим местом и полным набором услуг.',
    'Deluxe':   'Просторный номер «Делюкс» с панорамным видом и VIP-сервисом.',
}


def category_list(request):
    """
    Список всех категорий с подсчётом total/booked/available.
    """
    check_in  = request.GET.get('check_in')  or date.today().isoformat()
    check_out = request.GET.get('check_out') or (date.today() + timedelta(days=1)).isoformat()

    # Группируем по kind, считаем общее и забронированное количество
    qs = (
        Room.objects
        .values('kind')
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
        # Собираем превью-картинки из static/images/categories/<kind_lower>/
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'categories', kind.lower())
        imgs = []
        if os.path.isdir(static_dir):
            for fn in sorted(os.listdir(static_dir)):
                if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    imgs.append(settings.STATIC_URL + f'images/categories/{kind.lower()}/{fn}')

        # Берём любое (sample) значение остальных полей из первой комнаты этой категории
        sample = Room.objects.filter(kind=kind).first()

        categories.append({
            'kind':        kind,
            'total':       c['total'],
            'available':   c['available'],
            'description': CATEGORY_DESCRIPTIONS.get(kind, ''),
            'area':        getattr(sample, 'area', ''),
            'bed_type':    getattr(sample, 'bed_type', ''),
            'parking':     getattr(sample, 'parking', ''),
            'tv':          getattr(sample, 'tv', ''),
            'air_conditioning': getattr(sample, 'air_conditioning', ''),
            'wifi':        getattr(sample, 'wifi', ''),
            'iron':        getattr(sample, 'iron', ''),
            'images':      imgs,
            'url':         reverse('booking:rooms_by_category', args=[kind]) +
                           f'?check_in={check_in}&check_out={check_out}',
        })

    # Порядок вывода категорий (можно изменить)
    ORDER = ['Standard','Family','Suite','Business','Deluxe']
    categories.sort(key=lambda x: ORDER.index(x['kind']) if x['kind'] in ORDER else len(ORDER))

    return render(request, 'booking/category_list.html', {
        'categories': categories,
        'check_in':   check_in,
        'check_out':  check_out,
    })


def rooms_by_category(request, kind):
    """
    Подробная страница конкретной категории:
    — слайдер картинок из static/images/categories/<kind>/
    — подробная информация
    — подсчёт total/booked/available из Room.objects.filter(kind=kind)
    """
    check_in  = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    # Коллекция всех комнат данного kind
    qs = Room.objects.filter(kind=kind)
    if not qs.exists():
        return render(request, '404.html', status=404)

    sample = qs.first()  # безопасно берём первую, чтобы взять поля area, bed_type и т.д.

    total = qs.count()
    if check_in and check_out:
        booked = qs.filter(
            booking__check_in__lt=check_out,
            booking__check_out__gt=check_in
        ).count()
    else:
        booked = 0
    available = total - booked

    # Слайдер картинок из папки static/images/categories/<kind_lower>/
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'categories', kind.lower())
    images = []
    if os.path.isdir(static_dir):
        for fn in sorted(os.listdir(static_dir)):
            if fn.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                images.append(settings.STATIC_URL + f'images/categories/{kind.lower()}/{fn}')

    return render(request, 'booking/rooms_by_category.html', {
        'kind':        kind,
        'images':      images,
        'description': CATEGORY_DESCRIPTIONS.get(kind, ''),
        'area':        sample.area,
        'bed_type':    sample.bed_type,
        'parking':     sample.parking,
        'tv':          sample.tv,
        'air_conditioning': sample.air_conditioning,
        'wifi':        sample.wifi,
        'iron':        sample.iron,
        'total':       total,
        'available':   available,
        'check_in':    check_in,
        'check_out':   check_out,
    })
def room_detail(request, kind, pk):
    check_in  = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    room = get_object_or_404(Room, pk=pk, kind=kind)
    media_dir = os.path.join(settings.MEDIA_ROOT, 'rooms', str(room.number))
    imgs = []
    if os.path.isdir(media_dir):
        for fn in sorted(os.listdir(media_dir)):
            if fn.lower().endswith(('.jpg','jpeg','png','gif')):
                imgs.append(settings.MEDIA_URL + f'rooms/{room.number}/{fn}')

    return render(request, 'booking/room_detail.html', {
        'room':      room,
        'images':    imgs,
        'check_in':  check_in,
        'check_out': check_out,
    })
