import mysockets
import threading
import datetime
import time


class SomeKind(mysockets.Server):
    def __init__(self):
        self.server_thread, self.server = None, None
        self.create_server_thread()
        self.generate_time()


    def create_server_thread(self):
        self.server_thread = threading.Thread(target=self.server)
        self.server_thread.start()

    def run_server(self):
        self.server = mysockets.Server()

    def generate_time(self):
        while True:
            my_time = 'my time is: ' + str(datetime.datetime.now())
            #return my_time
            print(my_time)
            time.sleep(1)


a = SomeKind()
