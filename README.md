# Django Tasks Manager

Just a Simple Django & Celery integration.

<br />

## How to use it

<br />

> **Install the package** via `PIP` 

```bash
$ pip install django-tasks-manager
// OR
$ pip install git+https://github.com/app-generator/django-tasks-manager.git
```

<br />

> `Update Configuration`: Include the new templates 

```python
TEMPLATE_DIR_TASKS = os.path.join(BASE_DIR, "django_tm/templates")     # <-- NEW

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',   
        'DIRS': [TEMPLATE_DIR, TEMPLATE_DIR_TASKS],                    # <-- Updated
        'APP_DIRS': True,
    },
]
```

<br />

> `Update Configuration`: New **CELERY_** Section

```python

#############################################################
# Celery configurations
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

CELERY_SCRIPTS_DIR        = os.path.join(BASE_DIR, "django_tm", "celery_scripts" )
CELERY_LOGS_DIR           = os.path.join(BASE_DIR, "django_tm", "celery_logs"    )

CELERY_BROKER_URL         = os.environ.get("CELERY_BROKER", "redis://localhost:6379")
CELERY_RESULT_BACKEND     = os.environ.get("CELERY_BROKER", "redis://localhost:6379")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT    = 30 * 60
CELERY_CACHE_BACKEND      = "django-cache"
CELERY_RESULT_BACKEND     = "django-db"
CELERY_RESULT_EXTENDED    = True
CELERY_RESULT_EXPIRES     = 60*60*24*30 # Results expire after 1 month
CELERY_ACCEPT_CONTENT     = ["json"]
CELERY_TASK_SERIALIZER    = 'json'
CELERY_RESULT_SERIALIZER  = 'json'

#############################################################
#############################################################

```

<br />

> **Start the app**

```bash
$ # Set up the database
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Create the superuser
$ python manage.py createsuperuser
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
```

Access the `Tasks` page: `http://127.0.0.1:8000/tasks`

<br />

## Screenshots

@Todo

<br />

---
Django Tasks Manager - Open-source library provided by **[AppSeed](https://appseed.us/)**
