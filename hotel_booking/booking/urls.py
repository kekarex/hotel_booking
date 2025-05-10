from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path('',                         views.category_list,      name='category_list'),
    path('category/<str:kind>/',     views.rooms_by_category, name='rooms_by_category'),
    path('room/<int:pk>/',           views.room_detail,       name='room_detail'),
]
