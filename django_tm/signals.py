# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, json

from django_celery_results.models import TaskResult
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings


@receiver(pre_save, sender=TaskResult)
def pre_result_updated(sender, **kwargs):
    '''
    Before a task result is saved, the following checks and updates are carried out if task is complete:
    - Check if error key & value exist in result.result, if yes upate instance.status=`FAILURE` and instance.traceback=`logs produced during task execution`
    '''
    if 'instance' not in kwargs:
        return
    instance = kwargs.pop("instance")
    if instance.status != "STARTED":
        result = json.loads(instance.result)
        if result.get("error"):
            instance.status = "FAILURE"
            instance.traceback = result.get("logs")


@receiver(post_save, sender=TaskResult)
def post_result_updated(sender, **kwargs):
    """
    After a task is completed, we store its logs in a file.
    """
    if 'instance' not in kwargs:
        return
    instance = kwargs.pop("instance")
    if instance.status != "STARTED":
        add_log(instance)


def add_log(result: TaskResult):
    """
    Adds log file to celery logs with formatted date as name.
    :param result TaskResult: Result of executed celery task
    :rtype: None
    """
    if not result.task_name:
        return

    try:

        log_file_path = os.path.join(
                settings.CELERY_LOGS_DIR, f"{result.date_created.strftime(r'%Y%m%d-%H_%M')}-{result.task_id}-{result.status}.log")

        with open(log_file_path, "w+") as f:
            if result.status == "FAILURE":
                f.writelines([result.result, result.traceback])
            else:
                f.write(result.result)

            f.close()

    except Exception as e:
        print( 'Logging ERR: ' + str( e) )
        return
        