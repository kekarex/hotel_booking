from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, '★'*i + '☆'*(5-i)) for i in range(1,6)]),
            'text': forms.Textarea(attrs={'rows':4, 'placeholder':'Ваш отзыв...'}),
        }
        labels = {
            'rating': 'Ваша оценка',
            'text': 'Отзыв',
        }
