import datetime
import time
from threading import Thread


class CBit:

    def __init__(self, clock_rate=500):
        self.clock_rate = clock_rate
        self.processes = []
        self.thread = Thread(name='CBit_thread', target=self.run_processes)
        self.thread.start()
        print('CBit started at %d milli-second' % self.clock_rate)

    def run_processes(self):
        while True:
            for current_process in self.processes:
                current_process(**self.kwargs)
            time.sleep(self.clock_rate / 1000)

    def append_process(self, p, **kwargs):
        self.kwargs = kwargs
        self.processes.append(p)

    def remove_process(self, p):
        del self.processes[self.processes.index(p)]


def print_hi(x, y):
    print(datetime.datetime.now(), x, y)


def print_OK():
    print('OK')


a = CBit(500)

a.append_process(print_hi, x=1, y=2)
