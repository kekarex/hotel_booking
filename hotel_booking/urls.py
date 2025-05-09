from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Встроенные view для логина/логаута
    path('accounts/', include('django.contrib.auth.urls')),
    # Приложение пользователей
    path('users/', include('users.urls', namespace='users')),
    # Статические страницы (главная, о нас, услуги)
    path('', include('pages.urls', namespace='pages')),
    # Бронирование комнат
    path('booking/', include('booking.urls', namespace='booking')),
]
