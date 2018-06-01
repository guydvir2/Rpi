import socket
import threading
import time


class Server:

    def __init__(self, host='localhost', port=4001):
        self.host, self.port = host, port
        self.conn, self.addr, self.out_data = None, None, ''
        self.mySocket = socket.socket()
        self.mySocket.bind(('', self.port))
        self.t = threading.Thread(name='mysockets.Server', target=self.wait_for_conn)
        self.t.start()

    def wait_for_conn(self):
        while True:
            try:
                self.mySocket.listen(1)
                self.conn, self.addr = self.mySocket.accept()
                input_from_client = self.conn.recv(1024).decode()
                data_to_return = self.query_server(input_from_client)

                if type(data_to_return) == list:
                    for data in data_to_return:
                        self.out_data = self.out_data + ';' + str(data)
                elif type(data_to_return) != list:
                    print("not_list")
                    self.out_data = str(data_to_return)

                self.conn.send(self.out_data.encode())
                self.conn.close()

            except KeyboardInterrupt:
                print("Abort by user")
                quit()

    def query_server(self, input_from_client=None):
        if input_from_client is None:
            return "Ask Nothing- get Nothing"
        else:
            return '0'


class Client:
    def __init__(self, host='127.0.0.1', port=4001):
        self.host, self.port = host, port
        self.mySocket = socket.socket()
        self.mySocket.connect((self.host, self.port))

    def send_msg(self, message):
        message = str(message)
        self.mySocket.send(message.encode())
        data = self.mySocket.recv(1024).decode()
        print('Received from server: ' + data)
        self.mySocket.close()


if __name__ == "__main__":
    try:
        s = Server()
        while True:
            print("HI")
            time.sleep(1)
    except KeyboardInterrupt:
        s.mySocket.close()
