import socket
import time


class Server:

    def __init__(self, host="127.0.0.1", port=5000):
        self.host, self.port = host, port
        self.mySocket = socket.socket()
        self.mySocket.bind((self.host, self.port))

        self.start_listening()

    def start_listening(self):
        self.mySocket.listen(1)
        self.conn, self.addr = self.mySocket.accept()

        print("Connection from: " + str(self.addr))
        while True:
            data = self.conn.recv(1024).decode()
            if not data:
                break
            print("from connected  user: " + str(data))

            data = str(data).upper()
            print("sending: " + str(data))
            self.conn.send(data.encode())

        self.conn.close()


class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host, self.port = host, port
        self.mySocket = socket.socket()
        self.mySocket.bind((self.host, self.port))

    def send_msg(self, message):
        # while message != 'q':
        while True:
            self.mySocket.send(message.encode())
            data = self.mySocket.recv(1024).decode()
            print('Received from server: ' + data)
        self.mySocket.close()


if __name__ == "__main__":
    s = Server()
