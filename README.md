# Django Tasks Manager

A super simple **Django & Celery** integration - This library is actively supported by [AppSeed](https://appseed.us/).

> Features: 

- Create/Revoke Celery Tasks
- View LOGS & Output
- Minimal Configuration
- Installation via PyPi
- Available [TASKS](https://github.com/app-generator/django-tasks-manager/blob/main/django_tm/tasks.py) (provided as starting samples)
  - `users_in_db()` - List all registered users
  - `execute_script()` - let users execute the [scripts](https://github.com/app-generator/django-tasks-manager/tree/main/django_tm/celery_scripts) defined in `CELERY_SCRIPTS_DIR` (configuration parameter)
    - [check-db-health.py](https://github.com/app-generator/django-tasks-manager/blob/main/django_tm/celery_scripts/check-db-health.py) (sample)    
    
<br />    

> Something is not yet provided? [Open a PR](https://github.com/app-generator/django-tasks-manager/issues) on the repository orcontribute via a `fork`.

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

> **Include the new routing**

```python
# core/urls.py

from django.urls import path, include     # <-- UPDATE: Add 'include' HELPER

urlpatterns = [
    ...
    
    path("", include("django_tm.urls")),  # <-- New Routes

    ...
]
```

<br />

> Create **Scrips & LOGS** directories - The Recomended place is in the root of the project:

```bash
$ mkdir celery_scripts # Used in Settings -> CELERY_SCRIPTS_DIR
$ mkdir celery_logs    # Used in Settings -> CELERY_SCRIPTS_DIR
```

- Make sure the user that executes the app has write permission. 
- Copy the [sample scripts](./django_tm/celery_scripts) in the scripts directory. 
- All scripts will be available in the UI, ready to be executed by the manager. 

<br />

> **Update Configuration**: Include the new APPS

```python
INSTALLED_APPS = [
    ...                  
    'django_tm',              # Django Tasks Manager   # <-- NEW
    'django_celery_results',  # Django Celery Results  # <-- NEW
]
```

<br />

> **Update Configuration**: Include the new templates 

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

> **Update Configuration**: New **CELERY_** Section

```python

#############################################################
# Celery configurations
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

# BASE_DIR points to the ROOT of the project
# Note: make sure you have 'os' object imported
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Working Directories required write permission
CELERY_SCRIPTS_DIR        = os.path.join(BASE_DIR, "celery_scripts" )
CELERY_LOGS_DIR           = os.path.join(BASE_DIR, "celery_logs"    )

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

> **Start the App** 

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

> **Start the Celery Manager** (another terminal)

**Note**: `Redis` server is expected on port `6379` (default). In case Redis runs on other `PORT`, please update the configuration: `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`.

```bash
$ celery --app=django_tm.celery.app worker --loglevel=info 
``` 

<br />

## Screens

> `View all tasks`

![Django Tasks Manager - View All Tasks.](https://user-images.githubusercontent.com/51070104/195669853-677e887e-f8b2-4b56-bcf3-f81d98b175b0.jpg)

<br />

> `View Task LOG`

![Django Tasks Manager - View Task LOG.](https://user-images.githubusercontent.com/51070104/195669981-c64e3d13-1d83-496a-b527-cade9cda2cd2.jpg)

<br />

> `View Running Tasks`

![Django Tasks Manager - View Running Tasks.](https://user-images.githubusercontent.com/51070104/195670211-a24f7d72-37c1-48fc-a842-ab45b4559ca0.jpg)

<br />

---
Django Tasks Manager - Open-source library provided by **[AppSeed](https://appseed.us/)**
