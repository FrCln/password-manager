# -*- coding: utf-8 -*-
from base_file import *

base_changed = False

def main():
    base = BaseFile()
    base.connect_yadisk()
    status = base.check_file()
    if status in (CLOUD_FILE_NEWER, NO_LOCAL_FILE):
        base.download_file()
    try:
        password = input('Введите пароль: ')
        base.read_file(password)
    except FileNotFoundError:
        base.create_base()

    while True:
        com = get_command()
        if com in funcs:
            funcs[com][0](base)
        else:
            print('Такой команды нет!')


def get_command():
    print('Введите команду:')
    for com in funcs:
        print(f'{com}. {funcs[com][1]}')

    return input()


def add_password(base):
    global base_changed
    serv = input('Введите название сервиса: ')
    if serv in base.passwords:
        answer = input(f'Запись {serv} уже есть. Перезаписать? (y/n) ')
        if answer.lower() != 'y':
            return
    login = input('Введите логин: ')
    pwd = input('Введите пароль: ')
    base.passwords[serv] = (login, pwd)
    base_changed = True


def get_password(base):
    serv = input('Введите название сервиса: ')
    try:
        login, password = base.passwords[serv]
        print(f'login={login}, password={password}')
    except KeyError:
        print(f'Записи {serv} не найдено')


def get_base(base):
    print('\n'.join(base.passwords.keys()))


def quit(base):
    if base_changed:
        base.save_file()
        base.upload_file()
    exit()


funcs = {
    '1': (add_password, 'Ввести новый пароль'),
    '2': (get_password, 'Получить пароль из базы'),
    '3': (get_base, 'Получить список сервисов'),
    '4': (quit, 'Выход')
}
main()
