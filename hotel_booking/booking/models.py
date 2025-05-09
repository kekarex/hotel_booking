from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Room(models.Model):
    """Номер отеля"""
    number = models.CharField('Номер', max_length=10, unique=True)
    kind = models.CharField('Категория', max_length=50)
    price = models.DecimalField('Цена за ночь', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f"{self.kind} №{self.number}"

class Booking(models.Model):
    """Бронирование пользователя"""
    user = models.ForeignKey(User, verbose_name='Гость', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name='Номер', on_delete=models.CASCADE)
    check_in = models.DateField('Заезд')
    check_out = models.DateField('Выезд')
    created_at = models.DateTimeField('Забронировано', auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        # гарантируем отсутствие двойных бронирований одного номера
        unique_together = ('room', 'check_in', 'check_out')

    def clean(self):
        # check that dates make sense
        if self.check_out <= self.check_in:
            raise ValidationError('Дата выезда должна быть после даты заезда.')
        # overlapping bookings
        overlapping = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError('Номер уже забронирован на выбранные даты.')

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)