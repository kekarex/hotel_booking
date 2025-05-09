from django.urls import path
from .views import home, about, services, reviews, contacts

app_name = 'pages'
urlpatterns = [
    path('',        home,     name='home'),
    path('about/',  about,    name='about'),
    path('services/', services, name='services'),
    path('reviews/', reviews,  name='reviews'),
    path('contacts/', contacts,name='contacts'),
]
