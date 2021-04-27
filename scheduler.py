from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from helper import startProcess

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=20, minute='12')
def scheduled_job():
    startProcess()

sched.start()
