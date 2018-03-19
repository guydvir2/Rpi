import time
import datetime
import threading


def do_your_thing():
    try:
        while True:
            print(threading.currentThread().getName(),str(datetime.datetime.now())[:-7])
            time.sleep(1)
    except KeyboardInterrupt:
        print("Forced by user")

t = threading.Thread(name='Thread_1', target=lambda: do_your_thing())
t.start()

