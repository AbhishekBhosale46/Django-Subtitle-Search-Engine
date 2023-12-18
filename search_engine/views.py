from django.shortcuts import render, redirect
from .forms import UploadVideoForm
from . import tasks

def home(request):
    return render(request, 'search_engine/home.html')

def upload_video(request):

    if request.method == 'POST':

        form = UploadVideoForm(request.POST, request.FILES)

        if form.is_valid():

            """ Extract neccessary details """
            video_file = request.FILES['file']
            video_file_name = str(video_file).split('.')[0]
            video_file_extension = str(video_file).split('.')[1]

            """ Store the video temporarily in media directory """
            temp_video_file_path = f'media/{video_file_name}.{video_file_extension}'
            with open(temp_video_file_path, 'wb') as temp_video_file:
                for chunk in video_file.chunks():
                    temp_video_file.write(chunk)

            """ Enqueue the task into task queue (redis) """
            tasks.process_video.delay(video_file_name, video_file_extension)

            return redirect('home')
    else:
        form = UploadVideoForm()

    return render(request, 'search_engine/upload_video.html', {'form': form})

def search_video(request):
    return render(request, 'search_engine/search_video.html')