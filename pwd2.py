# -*- coding: utf-8 -*-

base_changed = False


def main():
    funcs = {
        '1': (add_password, 'Ввести новый пароль'),
        '2': (get_password, 'Получить пароль из базы'),
        '3': (get_base, 'Получить список сервисов'),
        '4': (quit, 'Выход')
    }
    passwords = {}

    read_file()

    while True:
        com = get_command()
        if com in funcs:
            funcs[com][0]()
        else:
            print('Такой команды нет!')


def get_command():
    print('Введите команду:')
    for com in funcs:
        print(f'{com}. {funcs[com][1]}')

    return input()


def read_file():
    try:
        with open('pwd.txt') as f:
            for line in f.readlines():
                s, p = line.strip().split(',')
                passwords[s] = p
    except FileNotFoundError:
        answer = input('Файл базы не найден. Создать новый? (y/n) ')
        if answer.lower() != 'y':
            exit()
    except ValueError:
        answer = input('Файл базы испорчен. Создать новый? (y/n) ')
        if answer.lower() != 'y':
            exit()


def save_file():
    with open('pwd.txt', 'w') as f:
        for serv, pwd in passwords.items():
            f.write(f'{serv},{pwd}\n')


def add_password():
    global base_changed
    serv = input('Введите название сервиса: ')
    if serv in passwords:
        answer = input(f'Запись {serv} уже есть. Перезаписать? (y/n) ')
        if answer.lower() != 'y':
            return
    pwd = input('Введите пароль: ')
    passwords[serv] = pwd
    base_changed = True


def get_password():
    serv = input('Введите название сервиса: ')
    try:
        print(passwords[serv])
    except KeyError:
        print(f'Записи {serv} не найдено')


def get_base():
    print('\n'.join(passwords.keys()))


def quit():
    if base_changed:
        save_file()
    exit()

main()
