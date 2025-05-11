# pages/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import redirect_to_login
from .models import Review
from .forms import ReviewForm

def home(request):
    """
    Главная страница.
    """
    return render(request, 'pages/home.html')

def about(request):
    """
    Страница «О нас».
    """
    return render(request, 'pages/about.html')

def services(request):
    services_list = [
        'Завтрак «Шведский стол»',
        'Парковка',
        'Бассейн',
        'СПА-центр',
        'Тренажёрный зал',
        'Трансфер до аэропорта (по запросу)',
        'Ресторан и бар',
        'Консьерж-сервис',
        # 'Wi-Fi (удалено по просьбе)',  ← убрали
    ]
    return render(request, 'pages/services.html', {
        'services': services_list
    })

def reviews(request):
    reviews_qs = Review.objects.all()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.save()
            return redirect('pages:reviews')
    else:
        form = ReviewForm()

    # Добавляем в контекст список [1,2,3,4,5]
    context = {
        'reviews': reviews_qs,
        'form': form,
        'star_range': range(1, 6),
    }
    return render(request, 'pages/reviews.html', context)

def contacts(request):
    """
    Страница «Контакты».
    """
    return render(request, 'pages/contacts.html')
