import socket

HOST = 'localhost'
PORT = 6668

exit = ''
while exit == '':

	sock = socket.socket()
	sock.connect((HOST, PORT))
	'''
	Проверка существования пользователя, если есть, то вводим пароль. 
	Если правильно, то разрешаем вводить команды, но все действия может выполнять только в своей папке
	'''
	login = input('Введите свой логин: ')
	sock.send(login.encode())
	login_answer = sock.recv(1024).decode()
	#print(login_answer)
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
	    request = input('>')
	    if request == "exit":
	    	exit = 'выходим'
	    	request = 'exit'
	    	sock.send(request.encode())
	    	sock.close()
	    	print(f"Досвидания, {name}, надеемся ты скоро вернешься!")
	    	break 

	    sock.send(request.encode())
	    response = sock.recv(1024).decode()
	    print(response)
	    
	    
	    #sock.close()