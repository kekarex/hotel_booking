from django import forms
from .models import Booking
from django.forms.widgets import DateInput

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': DateInput(attrs={'type':'date'}),
            'check_out': DateInput(attrs={'type':'date'}),
        }
        labels = {
            'check_in': 'Дата заезда',
            'check_out': 'Дата выезда',
        }