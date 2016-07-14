#coding=utf-8
#!/usr/bin/python

from celery import Celery
import requests
import os
from db.infodb import update_pic
URLPIC = "http://192.168.50.128/angular/picture/"
PICDIR = "/home/gfshi/github/angular/picture"

app = Celery(
    "tasks",
    backend="redis://localhost:6379/2",
    broker="redis://localhost:6379/1")


def getSuffix(url):
    url_list = url.split("/")
    last = url_list[len(url_list) - 1]
    index = last.find(".")
    if index != -1:
        return url[index + 1:]
    index = last.find("wx_fmt")
    if index != -1:
        return last[index + 7:]
    else:
        return None


@app.task
def downPic(url, name):
    uid = name
    resp = requests.get(url)
    suffix = getSuffix(url)
    url = None
    if resp.ok:
        if not suffix:
            filepath = os.path.join(PICDIR, name)
        else:
            filepath = os.path.join(PICDIR, name + "." + suffix)
            name = name + "." + suffix
        f = open(filepath, "w")
        f.write(resp.content)
        f.close()
        url = URLPIC + name
    print uid
    print update_pic(uid, {"url": url})
    return url
