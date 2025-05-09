from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Booking
from .forms import BookingForm


@login_required
def room_list(request):
    """
    Список доступных для бронирования комнат.
    """
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'booking/room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, pk):
    """
    Детали комнаты и форма бронирования.
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            # Обновляем доступность комнаты
            room.is_available = False
            room.save()
            booking.save()
            messages.success(request, 'Бронирование успешно создано!')
            return redirect('booking:room_list')
    else:
        form = BookingForm(initial={'room': room})
    return render(request, 'booking/room_detail.html', {'room': room, 'form': form})