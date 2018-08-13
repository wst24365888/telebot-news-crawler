import os
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
 
@sched.scheduled_job('interval', seconds=5)
def cr():
    print('Do crawler.')
    #os.system("python crawler.py")
 
sched.start()