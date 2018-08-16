import os
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

i = 1
 
@sched.scheduled_job('interval', seconds=300)
def cr():
    global i
    print('{}th time doing crawler.'.format(i))
    os.system("python crawler.py")
    i+=1

sched.start()