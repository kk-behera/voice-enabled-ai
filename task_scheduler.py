# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 00:42:43 2018

@author: Kamalakanta
"""

import schedule as sc, sched
#import mode_operations as mo

def sayHello():
    print("Hello")

# =============================================================================
# print(time.time())
# s = sched.scheduler(time.time,time.sleep)
# s.enterabs(time.clock,1,time.time())
# =============================================================================

sc.run_all()
a = sc.next_run()   
print(a)

sc.clear()
# =============================================================================
# dt = datetime.datetime.now()
# if dt.time() < datetime.time(12):
#     if dt.hour == 10 and dt.minute == 50:
#         print("It's morning")
# else:
#     print("It's afternoon")
#     
# print(dt.time + 2)
# =============================================================================
# =============================================================================
# def activateMode():
#     mo.activateRequestedMode("No",None)
# =============================================================================
