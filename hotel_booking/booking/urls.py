from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'booking'
urlpatterns = [
    path('',                         views.category_list,      name='category_list'),
    path('category/<str:kind>/',     views.rooms_by_category, name='rooms_by_category'),
    path('room/<int:pk>/',           views.room_detail,       name='room_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)