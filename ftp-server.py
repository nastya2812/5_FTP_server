import socket
import os
import shutil

"""
pwd - посмотреть в какой директории находишься ты
ls - посмотреть, что находится в директории
mkfile - создать файл 
cat - открыть файл и получить его данные
mkdir - создать директорию
rmdir - удалить директорию
remove - удалить файл
rename - переименовать файл
exit - выход с сервера
"""

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req[0:6] == 'mkfile':
        if os.path.isfile(dirname+'/'+req[7:]):
            return "Файл с таким именем уже есть!"
        else:
            f = open(dirname+'/'+req[7:], 'w')
            f.close()
            return "Файл создан!"
    elif req[0:3] == 'cat':
        try:
            f = open(os.path.join(os.path.join(os.getcwd(), 'docs'),req[4:]),'r')
        except:
            return 'Нет такого файла'
        answer = ''
        for line in f:
            line.strip('\n')
            answer += line
        return answer
    elif req[0:5] == 'mkdir':
    	try:
    		os.mkdir(dirname+'/'+req[6:])
    		return 'Директория с названием {} успешно создана!'.format(req[6:])
    	except:
    		return 'Такая директория уже создана' 
    elif req[0:5] == 'rmdir': 
    	try:
    		shutil.rmtree(dirname+'/'+req[6:]) 
    		return 'Директория с названием {} успешно удалена!'.format(req[6:])
    	except:
    		return 'Не удалось удалить директорию {}'.format(req[6:]) 
    elif req[0:6] == 'remove':
        try:
            os.remove(dirname+'/'+req[7:])
            return 'Файл с названием {} успешно удален!'.format(req[7:])
        except:
            return 'Не удалось удалить файл. Возможно файла с таким именем не существует' 
    elif req[0:6] == 'rename':
        spic = req.split(" ")
        try:
            os.rename(dirname+'/'+spic[1],dirname+'/'+spic[2])
            return 'Файл переименован!'
        except:
            return 'Не удалось переименовать файл' 
    elif req[0:4] == 'exit':
        return "Досвидания, надеемся ты скоро вернешься!"
    return 'bad request'

PORT = 6668

sock = socket.socket()
sock.bind(('', PORT))   
sock.listen()
print('Прослушиваем порт', PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    responce = process(request)
    conn.send(responce.encode())

conn.close()