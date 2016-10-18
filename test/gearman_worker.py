#coding=utf-8
#!/usr/bin/python

import gearman


def work(msg):
    return msg


def worker():
    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    gm_worker.register_task('index', work)
    gm_worker.work()


if __name__ == "__main__":
    worker()
