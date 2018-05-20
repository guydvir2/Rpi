import socket
import threading


class Server:

    def __init__(self, host="127.0.0.1", port=4001):
        self.host, self.port = host, port
        self.mySocket = socket.socket()
        # self.mySocket.bind((self.host, self.port))
        self.mySocket.bind(('', self.port))
        self.t = threading.Thread(name='mysockets.Server', target=self.run_connection_server())
        self.t.start()
        # self.p1='100'
        # self.p2=200
        # self.p3="GUYDVIR"

    def run_connection_server(self):
        while True:
            self.wait_for_conn()

    def wait_for_conn(self):
        try:
            self.mySocket.listen(1)
            self.conn, self.addr = self.mySocket.accept()
            recv_data = self.conn.recv(1024).decode()
            send_data = self.transfer_data(recv_data)
            self.conn.send(send_data.encode())
            self.conn.close()
        except KeyboardInterrupt:
            print("keyboard")


    def transfer_data(self, recv_data):
        if recv_data == '1':
            return "KUKU"
        elif recv_data == '2':
            return ["BUBU",'sdfsdfsdf']
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
    s = Server()
    # c = Client()
    # c.send_msg('hi')
