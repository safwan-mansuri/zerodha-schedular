from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from helper import startProcess

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=2)
def scheduled_job():
  startProcess()

sched.start()
