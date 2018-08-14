import os
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
 
@sched.scheduled_job('interval', seconds=30)
def cr():
    print('Do crawler.')
    os.system("python crawler.py")
 
sched.start()