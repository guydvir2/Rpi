import mysockets
import datetime
from time import sleep


class Counter(mysockets.Server):
    def __init__(self):
        mysockets.Server.__init__(self)
        self.output = None
        self.run()

    def run(self):
        for x in range(1000):
            self.output = (str(datetime.datetime.now()), str(x))
            sleep(1)

    def query_server(self, input_from_client=None):
        if input_from_client == '1':
            return self.output


a = Counter()
