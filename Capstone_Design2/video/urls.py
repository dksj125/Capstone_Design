# video/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='list')
]