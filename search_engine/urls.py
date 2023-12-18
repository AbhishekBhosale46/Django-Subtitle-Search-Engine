from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.home, name='home'),
    path('upload/', view=views.upload_video, name='upload_video'),
    path('search/<int:id>', view=views.search_video, name='search_video'),
    path('videos/', view=views.list_videos, name='list_videos'),
]