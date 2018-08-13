import os
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
 
@sched.scheduled_job('interval', minutes=3)
def cr():
    print('Do crawler.')
    os.system("python crawler.py")
 
sched.start()