from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import datetime
from helper import startProcess

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=18)
def scheduled_job():
    startProcess()

sched.start()
