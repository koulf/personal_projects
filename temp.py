import time

proceed = True
duration = 3

def elapse():
    global duration
    while duration > 0:
        duration -= 1
        time.sleep(1)
    return proceed

if elapse():
    print("yei")
else:
    print("ahh")