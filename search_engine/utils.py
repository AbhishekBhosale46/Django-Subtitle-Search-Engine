import subprocess
import webvtt
import json
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def extract_subtitles(file_name, file_extension):

    """ Extract the subtitles"""
    subprocess.run(['CCExtractor_win_portable\ccextractorwinfull.exe', f'media/{file_name}.{file_extension}', '-o', f'media/{file_name}.srt'])
    print('EXTRACTED SRT')

    """ Convert .srt to .vtt """
    vttfile = webvtt.from_srt(f'media/{file_name}.srt')
    vttfile.save(f'media/{file_name}.vtt')
    print('CONVERTED TO VTT')

    """" Convert .vtt to .json """
    subprocess.run(['webvtt-to-json', '--dedupe', '--single', f'media/{file_name}.vtt', '-o', f'media/{file_name}.json'])
    print('CONVERTED TO JSON')

def upload_to_s3(file_name, file_extension):
    s3 = boto3.resource(
        service_name = 's3',
        region_name = os.getenv('AWS_REGION_NAME'),
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    response = s3.Bucket(os.getenv('S3_BUCKET_NAME')).upload_file(Filename=f'media/{file_name}.{file_extension}', Key=file_name)
    print(response)
    print('DONE S3')

def upload_to_dynamodb(file_name):
    dynamodb = boto3.resource(
        service_name = 'dynamodb',
        region_name = os.getenv('AWS_REGION_NAME'),
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))
    with open(f'media/{file_name}.json', 'r') as jsonFile:
        jsonData = json.load(jsonFile)
    id = 1
    for data in jsonData:
        item = {
            'video_name': file_name,
            'id': id,
            'start': data['start'],
            'end': data['end'],
            'line': data['line']
        }
        table.put_item(Item=item)
        id += 1
    print('DONE DYNAMODB')