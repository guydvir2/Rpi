import socket
 
def Main():
        host = '127.0.0.1'
        port = 0
        
         
        mySocket = socket.socket()
        mySocket.connect((host,5000))
        user1=input("type usename:") 
        message = input("%s: "%user1)
        
        while message != 'q':
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()
                 
                print ('Received from server: ' + data)
                 
                message = input("%s: "%user1)
                 
        mySocket.close()
 
if __name__ == '__main__':
    Main()
