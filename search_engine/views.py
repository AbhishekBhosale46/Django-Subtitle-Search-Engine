from django.shortcuts import render

def home(request):
    return render(request, 'search_engine/home.html')

def upload_video(request):
    return render(request, 'search_engine/upload_video.html')

def search_video(request):
    return render(request, 'search_engine/search_video.html')