from django.db import models

class Video(models.Model):
    video_name = models.CharField(max_length=255)
