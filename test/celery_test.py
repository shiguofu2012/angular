#!/usr/bin/python

from celery import Celery
import requests


app = Celery('tasks', backend="redis://localhost:6379/2", broker='redis://localhost:6379/1')


@app.task
def add(url):
    r = requests.get(url)
    return r.ok
