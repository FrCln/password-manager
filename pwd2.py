def get_command():
    print('Введите команду:')
    for com in funcs:
        print(f'{com}. {funcs[com][1]}')

    return input()


def read_file():
    with open('pwd.txt') as f:
        for line in f.readlines():
            s, p = line.strip().split(',')
            passwords[s] = p


def save_file():
    with open('pwd.txt', 'w') as f:
        for serv, pwd in passwords.items():
            f.write(f'{serv},{pwd}\n')


def add_password():
    serv = input('Введите название сервиса: ')
    pwd = input('Введите пароль: ')
    passwords[serv] = pwd # FIXIT


def get_password():
    serv = input('Введите название сервиса: ')
    print(passwords[serv]) # FIXIT


def quit():
    save_file()
    exit()


funcs = {
    '1': (add_password, 'Ввести новый пароль'),
    '2': (get_password, 'Получить пароль из базы'),
    '3': (quit, 'Выход')
}
passwords = {}

read_file()

while True:
    com = get_command()
    if com in funcs:
        funcs[com][0]()
    else:
        print('Такой команды нет!')
