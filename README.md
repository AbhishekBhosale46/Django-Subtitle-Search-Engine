# Subtitle Search Engine

Subtitle Search Engine is a powerful platform that allows you to upload, process, and search video time stamps effortlessly based on given subtitle search keywords.

## Features

- **Subtitle Extraction:** Use of ccextractor binary to extract subtitles directly from your uploaded videos.
  
- **Background Processing:** The Django framework, handles video processing as a background task using Celery workers. This ensures an efficient and user-friendly experience.

- **Secure Video Storage:** Processed videos are securely stored in Amazon S3, providing reliability and scalability to accommodate your storage needs.

- **Subtitle Indexing:** The system indexes the extracted subtitles into DynamoDB, allowing you to search for specific words or phrases within the video content.

- **Precise Timestamp Search:** Imagine uploading a music video and, with a simple search, discovering the exact time segments where your chosen phrases are mentioned.

## Technologies Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)

- **Django:** A Python web framework for developing the webapp.

- **Celery:** Distributed task queue system for background processing.

- **Redis:** Used as a message broker to store the tasks.

- **ccextractor:** A tool for extracting closed captions (subtitles) from video files.

- **Amazon S3:** Scalable object storage service for secure and efficient video storage.

- **DynamoDB:** Fully managed NoSQL database for indexing and quick retrieval of subtitle information.

[![system-diagram.png](https://i.postimg.cc/g2S8gZX9/system-diagram.png)](https://postimg.cc/w1N1v3QF)

## Usage

**1.** Upload your video on the platform.

**2.** The system will extract subtitles and process the video in the background.

**3.** Once processed, you can search for specific words or phrases within the video content.

**4.** Explore the precise time segments where your chosen phrases are mentioned.




## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`AWS_REGION_NAME`
`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`S3_BUCKET_NAME`
`DYNAMODB_TABLE_NAME`


## Run Locally

Clone the project

```bash
  git clone https://github.com/AbhishekBhosale46/Django-Subtitle-Search-Engine/
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run migrations

```bash
  python manage.py migrate
```

Start Celery worker for background tasks

```bash
  celery -A yourprojectname worker -P threads -l info
```

Run the Django server

```bash
  python manage.py runserver
```
