from django.urls import path
from . import views

urlpatters = [
    path('', views.home, name='home'),
    path('room/', views.room, name='room'),
]