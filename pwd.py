


while True:
    print('Введите команду:\n'
          '1. Ввести новый пароль\n'
          '2. Получить пароль из базы\n'
          '3. Выход')

    command = input()

    if command == '1':
        serv = input('Введите название сервиса: ')
        pwd = input('Введите пароль: ')
        with open('pwd.txt', 'a') as f:
            f.write(serv + ',' + pwd + '\n')
    elif command == '2':
        serv = input('Введите название сервиса: ')
        with open('pwd.txt') as f:
            for line in f.readlines():
                s, p = line.split(',')
                if s == serv:
                    print(p)
    elif command == '3':
        exit()
    print('\n')
