import socket
 
def Main():
    host = "127.0.0.1"
    port = 5000
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
    #guyprint (mySocket) 
    mySocket.listen(2)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    varz=["var1","var2","var3"]
    while True:
            data = conn.recv(1024).decode()
            if data in varz[0] :
               print("YES!")
            print(data.split(' '))
            if not data:
                    break
            print ("from connected  user: " + str(data))
             
            data = str(data[0:2]).upper()
            print ("sending: " + str(data))
            conn.send(data.encode())
             
    conn.close()
     
if __name__ == '__main__':
    Main()
