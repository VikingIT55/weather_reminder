# Weather Reminder App with Background Task Queues

## Overview

This Django project demonstrates how to implement background task processing using Celery. It includes features such as user management, subscription-based notifications, and integration with a weather API.

## Features

- User Authentication (Login and Registration)
- Background task processing with Celery
- Periodic and scheduled tasks with Celery Beat
- Weather API Integration
- User subscription management and notifications

## Project Structure

```
.
├── subscriptions/
│   ├── models.py
│   ├── tasks.py
│   ├── views.py
│   ├── serializers.py
│   ├── notifications.py
│   └── templates/
│       └── index.html
├── users/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── templates/
│       ├── login.html
│       └── register.html
├── weather_api/
│   ├── celery.py
│   ├── models.py
│   ├── tasks.py
│   ├── services.py
│   ├── views.py
│   └── serializers.py
├── weather_reminder/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.celery_worker
└── Dockerfile.celery_beat
```

## Setup

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd django_weather_reminder
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Database & Initial Setup

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Docker Setup (optional)

Run services using Docker Compose:

```bash
docker-compose up
```

### Running Celery Workers

Run Celery worker:

```bash
celery -A weather_api worker --loglevel=info
```

Run Celery Beat for scheduled tasks:

```bash
celery -A weather_api beat --loglevel=info
```

### Start Django Server

Start Django development server:

```bash
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Contributing

Contributions are welcomed. Feel free to submit pull requests or create issues.

## License

MIT License.
