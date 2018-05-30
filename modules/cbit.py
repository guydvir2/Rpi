import datetime
import time
from threading import Thread


class CBit:

    def __init__(self, clock_rate=500):
        self.clock_rate = clock_rate
        self.processes = []
        self.kwargs = []
        self.thread = Thread(name='CBit_thread', target=self.runProcesses)
        #print('CBit at %d milli-second' % self.clock_rate)

    def runProcesses(self):
        while True:
            for i, current_process in enumerate(self.processes):
                current_process(**self.kwargs[i])
            time.sleep(self.clock_rate / 1000)

    def append_process(self, p, **kwargs):
        self.kwargs.append(kwargs)
        self.processes.append(p)

    def remove_process(self, p):
        del self.processes[self.processes.index(p)]

    def get_status(self):
        return self.processes

    def init_thread(self):
        self.thread.start()

if __name__ == "__main__":
    def print_hi(x, y):
        print(datetime.datetime.now(), x, y)
        
    def print_OK():
        print('OK')

    a = CBit(50)
    a.append_process(print_hi, x=1, y=2)
    a.append_process(print_OK)
    a.init_thread()
