from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.home, name='home'),
    path('upload/', view=views.upload_video, name='upload_video'),
    path('search/', view=views.search_video, name='search_video'),
]