from celery import Celery

app = Celery('subtitle_search_engine')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

@app.task(bind=True, ignore_result=True)
def process_video(self, video_file_name):
    return "DONE PROCESSING "+video_file_name 