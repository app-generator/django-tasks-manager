# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, time, subprocess
from os import listdir
from os.path import isfile, join

from .celery import app
from celery.contrib.abortable import AbortableTask

from django.contrib.auth.models import User
from django.conf import settings

def get_scripts():
    """
    Returns all scripts from 'ROOT_DIR/celery_scripts'
    """
    try:
        scripts = [f for f in listdir(settings.CELERY_SCRIPTS_DIR) if isfile(join(settings.CELERY_SCRIPTS_DIR, f))]
        return scripts, None 
    except Exception as e:
        return None, 'Error CELERY_SCRIPTS_DIR: ' + str( e )    

@app.task(bind=True, base=AbortableTask)
def users_in_db(self, data: dict):
    """
    Outputs all users in DB
    :param data dict: contains data needed for task execution.
    :rtype: None
    """
    users = User.objects.all()
    return {"output": "\n".join([u.email for u in users])}

@app.task(bind=True, base=AbortableTask)
def execute_script(self, data: dict):
    """
    This task executes scripts found in settings.CELERY_SCRIPTS_DIR and logs are later generated and stored in settings.CELERY_LOGS_DIR
    :param data dict: contains data needed for task execution. Example `input` which is the script to be executed.
    :rtype: None
    """
    script = data.get("input")

    scripts, ErrInfo = get_scripts()

    if script and script in scripts:
        # Executing related script
        script_path = os.path.join(settings.CELERY_SCRIPTS_DIR, script)
        process = subprocess.Popen(
            f"python {script_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(8)
        error = False
        if process.wait() == 0:  # If script execution successfull
            logs = process.stdout.read().decode()
        else:
            logs = process.stderr.read().decode()
            error = True

        return {"logs": logs, "input": script, "error": error, "output": ""}
