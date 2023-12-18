from celery import Celery
from . import utils
import os

app = Celery('subtitle_search_engine')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

@app.task(bind=True, ignore_result=True)
def process_video(self, video_file_name, video_file_extension):

    utils.extract_subtitles(video_file_name, video_file_extension)

    utils.upload_to_s3(video_file_name, video_file_extension)

    utils.upload_to_dynamodb(video_file_name)
    
    """ Deleting the generated files after uploading """
    os.remove(f"media/{video_file_name}.{video_file_extension}")
    os.remove(f"media/{video_file_name}.srt")
    os.remove(f"media/{video_file_name}.vtt")
    os.remove(f"media/{video_file_name}.json")

    return "DONE PROCESSING "+video_file_name 