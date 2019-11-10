import logging

log_file = logging.FileHandler('myserver.log')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(log_file, console_out), format = '[%(asctime)s | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S' , level = logging.INFO)
logging.info('Start')


import socket
import os
import shutil

dirname=os.path.join(os.getcwd(),'docs')

def process(req, dirname):
    #Посмотреть текущую директорию
    if req =='pwd':
        return dirname
    
    #Посмотреть содержимое папки
    elif req =='ls':
        if os.listdir(dirname):
            return '; '.join(os.listdir(dirname))
        else:
            return 'Ничего нет в директории'
    
    #Посмотреть содержимое переданного файла
    elif req[:3]=='cat':
        mes=''
        testFile = os.path.join(dirname, req[4:])
        if os.path.isfile(testFile)==True:
            with open(testFile,'r+') as f:
                for line in f:
                    mes+=line
            return mes
        else:
            return "Failed filename!"
    
    #Создать файл
    elif req[:6]=='mkfile':
        testFile=os.path.join(dirname, req[7:])
        if os.path.isfile(testFile)==True:
            return "File is existed!"
        else:
            file = open(testFile, 'w')
            file.close()
            return "File was created!"
        
    
    #Создать папку
    elif req[:5]=='mkdir':
        path = os.path.join(dirname, req[6:])
        if os.path.exists(path) != True:
            os.mkdir(path)
            return "Path is ready, congradulations!"
        else:
            return "Path is existed!"
        
    #Удалить папку
    elif req[:5]=='rmdir':
        path = os.path.join(dirname, req[6:])
        if os.path.exists(path) == True:
            shutil.rmtree(path)
            return "Path was deleted!"
        else:
            return "Path isn't existed!"
        
    #Переименовать файл
    elif req[:2]=='rename':
        req=req.split(" ")
        old_file = os.path.join(dirname, req[1])
        new_file=os.path.join(dirname, req[2])
        if os.path.exists(old_file) == True:
            os.rename(old_file, new_file)
            return "File was renamed!"
        else:
           return "File isn't existed!" 
    
    
#    elif req.split(" ")[0] == 'copy.from':
#        req = req.split(" ")
#        if req[1] == 'client':
#            try:
#                with open(os.path.join(dirname, req[2]), "wb") as f:
#                   while True:
#                       data = conn.recv(1024)
#                       if data == b'sent':
#                            break
#                        f.write(data)
#                        return 'File was sent'
#            except IndexError:
#                return 'You did not type filename'
#        
#        elif req[1] == 'server':
#            try:
#                file = os.path.realpath(req[2])
#                with open(file, "rb") as f:
#                   data = f.read(1024)
#                    while data:
#                       conn.send(data)
#                       data = f.read(1024)
#                   conn.send(b'sent')
#                    return 'File was sent'
#           except IndexError:
#               return 'You did not type filename'
    
    else:
        return 'BAD REQUEST!'
    
    
PORT = 8081
sock = socket.socket()

sock.bind(('', PORT))
sock.listen()
logging.info(f"Слушаем порт {PORT}")

while True:
    conn, addr = sock.accept()
    
    login = conn.recv(1024).decode()
    print(login)
    login_est = 0
    with open(os.path.join(os.getcwd(), 'clients.txt'), 'r+') as file:
        for line in file:
            line = line.split(";")
            #если логин есть в строке
            if login == line[0]:
                login_est = 1
                #пока не введет праивльный пароль
                while True:
                    #отправляем сообщение
                    login_answer = 'Введите пароль'
                    conn.send(login_answer.encode())
                    #получаем пароль
                    passwd = conn.recv(1024).decode()
                    print(passwd)
                    #если пароль == паролю из строки, тогда отсылаем сообщение и выходим
                    if str(passwd) == str(line[1]):
                        prav_passwd = 'правильный пароль'
                        conn.send(prav_passwd.encode()) 
                        break
                break
        if login_est == 0: 
            login_answer = 'нет такого пользователя'
            conn.send(login_answer.encode()) 
            login_new_client = conn.recv(1024).decode()
            #Создаем папку для пользователя на клиенте
            os.mkdir(os.path.join(os.path.join(dirname, 'client'),login_new_client))
            passwd_new_client = conn.recv(1024).decode()
            file.write(f"{login_new_client};{passwd_new_client};\n")


    while True:
        dirname = os.path.join(os.getcwd(), 'docs')
        if login_est != 0:
            dirname = os.path.join(os.path.join(dirname,"client"),login)
        else:
            dirname = os.path.join(os.path.join(dirname,"client"),login_new_client)
        request = conn.recv(1024).decode()
        logging.info(request)
        if request == 'quit':
            break
        else:
            responce = process(request, dirname)
            conn.send(responce.encode())

conn.close()