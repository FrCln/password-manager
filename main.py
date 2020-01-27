# -*- coding: utf-8 -*-
import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

base_changed = False
salt = b'\x82\xe1\x85~!\xaf\xd5\xd2}\xbc#\xf0\x0f\xed\x02\xf9'
pwd = ''


def main():
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
    global pwd
    pwd = input('Введите пароль: ')
    global passwords
    try:
        with open('pwd.bin', 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        answer = input('Файл базы не найден. Создать новый? (y/n) ')
        if answer.lower() != 'y':
            exit()
        else:
            return
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd.encode(encoding='utf-8')))
    f = Fernet(key)
    try:
        data = f.decrypt(data)
    except InvalidToken:
        print('Неверный пароль!')
        exit()
    try:
        passwords = json.loads(data)
    except ValueError:
        answer = input('Файл базы испорчен. Создать новый? (y/n) ')
        if answer.lower() != 'y':
            exit()


def save_file():
    data = json.dumps(passwords).encode(encoding='utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd.encode(encoding='utf-8')))
    f = Fernet(key)
    with open('pwd.bin', 'wb') as file:
        file.write(f.encrypt(data))


def add_password():
    global base_changed
    serv = input('Введите название сервиса: ')
    if serv in passwords:
        answer = input(f'Запись {serv} уже есть. Перезаписать? (y/n) ')
        if answer.lower() != 'y':
            return
    login = input('Введите логин: ')
    pwd = input('Введите пароль: ')
    passwords[serv] = (login, pwd)
    base_changed = True


def get_password():
    serv = input('Введите название сервиса: ')
    try:
        login, password = passwords[serv]
        print(f'{login=}, {password=}')
    except KeyError:
        print(f'Записи {serv} не найдено')


def get_base():
    print('\n'.join(passwords.keys()))


def quit():
    if base_changed:
        save_file()
    exit()


funcs = {
    '1': (add_password, 'Ввести новый пароль'),
    '2': (get_password, 'Получить пароль из базы'),
    '3': (get_base, 'Получить список сервисов'),
    '4': (quit, 'Выход')
}
passwords = {}
main()
