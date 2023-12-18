from django.shortcuts import render, redirect
from .forms import UploadVideoForm
from . import tasks
from .models import Video
import boto3
import os
from dotenv import load_dotenv

dynamodb = boto3.resource(
    service_name = 'dynamodb',
    region_name = os.getenv('AWS_REGION_NAME'),
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
)
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))

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

            """ Store video name in local db """
            video = Video.objects.create(video_name=video_file_name)
            video.save()

            """ Enqueue the task into task queue (redis) """
            tasks.process_video.delay(video_file_name, video_file_extension)

            return redirect('home')
    else:
        form = UploadVideoForm()

    return render(request, 'search_engine/upload_video.html', {'form': form})

def list_videos(request):
    videos = Video.objects.all()
    return render(request, 'search_engine/list_videos.html', {'videos': videos})

def search_video(request, id):

    video = Video.objects.get(pk=id)

    if request.method == 'POST':

        search_keyword = request.POST.get('search_text', '')
        search_keyword = search_keyword.upper()
        response = table.scan(
            FilterExpression="contains(line, :keyword) AND video_name = :vname",
            ExpressionAttributeValues={":keyword": f"{search_keyword}", ":vname":f"{video.video_name}"}
        )
        
        if (response['Items']):
            response = (response['Items'])[0]
            start = response['start']
            end = response['end']
            context = {'video': video, 'start': start, 'end': end}
        else:
            print('Error occured')
            context = {'video': video, 'error': True}

        return render(request, 'search_engine/search_video.html', context) 

    context = {'video': video}
    return render(request, 'search_engine/search_video.html', context) 