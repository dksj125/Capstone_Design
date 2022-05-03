from django.shortcuts import render, redirect
from .models import Video


# Create your views here.
def video_list(request):
    video_list = Video.objects.all()
    return render(request, 'video/video_list.html', {'video_list':video_list})