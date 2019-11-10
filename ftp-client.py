import socket
import os

HOST='localhost'
try:
    PORT=int(input("port>:"))
    if not 0 <= PORT <= 65535:
        raise ValueError
except ValueError :
    PORT = 8081


while True:
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    login = input('Введите свой логин: ')
    sock.send(login.encode())
    login_answer = sock.recv(1024).decode()
    if login_answer == 'Введите пароль':
        name = login
        while True:
            passwd = input('Введите пароль: ')
            sock.send(passwd.encode())
            answer_passwd = sock.recv(1024).decode()
            if answer_passwd == 'правильный пароль':
                print('Пароль введен верно! Добро пожаловать, ' + login + '!')
                break
            else:
                print('Пароль введен неверно!')	
    else:
        new_login = input('Похоже вы еще не зарегестрированы, давайте создадим аккаунт! Введите логин: ')
        name = new_login
        sock.send(new_login.encode())
        new_passwd = input('Создайте пароль: ')
        sock.send(new_passwd.encode())
        print('Добро пожаловать, ' + new_login + '!')
        
    while True:   
        request = input(">")
        
        if request=='quit':
            sock.close()
            
#        elif request.split()[0] == "copy.from":
#            if request.split()[1] == 'client':
#                file = os.path.realpath(request.split()[2])
#                sock.send(f"copy.from client {request.split('/')[-1]}".encode())
#                with open(file, "rb") as f:
#                    data = f.read(1024)
#                    while data:
#                        sock.send(data)
#                        data = f.read(1024)
#                sock.send(b'sent')
#                print(sock.recv(1024).decode())
#            if request.split()[1] == 'server':
#                sock.send(request.encode())
#                with open(request.split('/')[-1], "wb") as f:
#                    while True:
#                        data = sock.recv(1024)
#                        if data == b'sent':
#                            break
#                        f.write(data)
#                response = sock.recv(1024).decode()
#                print(response)
            
        else:
            sock.send(request.encode())
            response=sock.recv(1024).decode()
            print(response)
    
    sock.close()