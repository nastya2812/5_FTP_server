import socket

HOST = 'localhost'
PORT = 6668

while True:
    request = input('>')

    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    if request == "exit":
    	sock.close()
    	break
    
    sock.close()