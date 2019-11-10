import socket
import os
import shutil

"""
pwd - посмотреть в какой директории находишься ты
ls - посмотреть, что находится в директории
mkfile < > - создать файл 
cat < >- открыть файл и получить его данные
mkdir < >- создать директорию
rmdir < >- удалить директорию
remove < >- удалить файл
rename < > < >- переименовать файл
exit - выход с сервера(выполняется на клиенте)
size_path < > - размер папки
cp_to_cl < > < > -
cp_to_srv < > - 
"""

dirname = os.path.join(os.getcwd(), 'docs')

def process(req, dirname):
    if req == 'pwd':
        dirname = dirname.lstrip('/')
        dirname = dirname.split('/')
        return '/' + dirname[5]
    elif req == 'ls':
        if os.listdir(dirname):
            return '; '.join(os.listdir(dirname))
        else:
            return 'Ничего нет в директории'
    elif req[0:6] == 'mkfile':
        if os.path.isfile(os.path.join(dirname,req[7:])):
            return "Файл с таким именем уже есть!"
        else:
            f = open(os.path.join(dirname, req[7:]), 'w')
            f.close()
            return "Файл создан!"
    elif req[0:3] == 'cat':
        try:
            f = open(os.path.join(dirname,req[4:]),'r')
        except:
            return 'Нет такого файла'
        answer = ''
        for line in f:
            line.strip('\n')
            answer += line
        return answer
    elif req[0:5] == 'mkdir':
    	try:
    		os.mkdir(os.path.join(dirname, req[6:]))
    		return 'Директория с названием {} успешно создана!'.format(req[6:])
    	except:
    		return 'Такая директория уже создана' 
    elif req[0:5] == 'rmdir': 
    	try:
    		shutil.rmtree(os.path.join(dirname, req[6:])) 
    		return 'Директория с названием {} успешно удалена!'.format(req[6:])
    	except:
    		return 'Не удалось удалить директорию {}'.format(req[6:]) 
    elif req[0:6] == 'remove':
        try:
            os.remove(os.path.join(dirname, req[7:]))
            return 'Файл с названием {} успешно удален!'.format(req[7:])
        except:
            return 'Не удалось удалить файл. Возможно файла с таким именем не существует' 
    elif req[0:6] == 'rename':
        spic = req.split(" ")
        try:
            os.rename(os.path.join(dirname, spic[1]),os.path.join(dirname,spic[2]))
            return 'Файл переименован!'
        except:
            return 'Не удалось переименовать файл' 
    elif req[0:9] == 'size_path':
        return str(os.path.getsize(os.path.join(dirname, req[10:])))
    #elif req[0:8] == 'cp_to_cl':
    #    req = req.split(' ')
    #    shutil.copy(req[1], req[2])
    #elif req[0:4] == 'exit':
     #   return "Досвидания, надеемся ты скоро вернешься!"
    return 'bad request'

PORT = 6668

sock = socket.socket()
sock.bind(('', PORT))   
sock.listen()
print('Прослушиваем порт', PORT)

while True:
    conn, addr = sock.accept()
    '''
    Просим пользователя ввести логин и пароль.
    Если такого пользователя нет, то создаем нового.
    '''
    #Получаем логин
    login = conn.recv(1024).decode()
    print(login)
    login_est = 0
    with open('/home/vlad/5_FTP_server/data.txt', 'r+') as file:
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
            dirname = dirname + "/client/"+ login
        else:
            dirname = dirname + "/client/"+ login_new_client
        request = conn.recv(1024).decode()
        print(request)
        if request == 'exit':
            break
        else:
            responce = process(request, dirname)
            conn.send(responce.encode())

conn.close()