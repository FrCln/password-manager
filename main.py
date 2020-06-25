# -*- coding: utf-8 -*-
import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime, timedelta, timezone
import os
import yadisk
import webbrowser


base_changed = False
salt = b'\x82\xe1\x85~!\xaf\xd5\xd2}\xbc#\xf0\x0f\xed\x02\xf9'
main_password = ''
yandex_disk = None


def main():
    connect_yadisk()
    download_file()
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


def connect_yadisk():
    global yandex_disk
    try:
        with open('yadisk-secret.txt') as f:
            application_id = f.readline().strip()
            application_secret = f.readline().strip()
            yadisk_token = f.readline().strip()

    except FileNotFoundError:
        print('Яндекс-диск недоступен')
        return

    if not yadisk_token:
        yandex_disk = yadisk.YaDisk(application_id, application_secret)
        url = yandex_disk.get_code_url()
        webbrowser.open(url)
        code = input('Введите код, полученный от Яндекс-диска: ')
        try:
            response = yandex_disk.get_token(code)
        except yadisk.exceptions.BadRequestError:
            print("Bad code")
            sys.exit(1)

        yadisk_token = yandex_disk.token = response.access_token
        with open('yadisk-secret.txt', 'a') as f:
            f.write('\n' + yadisk_token + '\n')

    else:
        yandex_disk = yadisk.YaDisk(token=yadisk_token)

    if not yandex_disk.check_token():
        print('Яндекс-диск недоступен')
        yandex_disk = None


def download_file():
    if not yandex_disk:
        return
    created = None
    for file in yandex_disk.listdir('app:/'):
        if file['name'] == 'pwd.bin':
            created = file['created']
    try:
        local_file_date = datetime.fromtimestamp(
            os.path.getmtime('pwd.bin'), timezone.utc
        )
    except FileNotFoundError:
        local_file_date = None
    if created is None:
        print('Файл в облаке отсутствует')
        return
    elif local_file_date is not None and created < local_file_date:
        print('Локальный файл новее, чем файл в облаке\n'
              'Загрузить более старый файл? [y/n]')
        answer = input()
        if answer == 'y':
            yandex_disk.download('app:/pwd.bin', 'pwd.bin')
    else:
        yandex_disk.download('app:/pwd.bin', 'pwd.bin')


def read_file():
    global main_password
    main_password = input('Введите пароль: ')
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
    key = base64.urlsafe_b64encode(kdf.derive(main_password.encode(encoding='utf-8')))
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
    key = base64.urlsafe_b64encode(kdf.derive(main_password.encode(encoding='utf-8')))
    f = Fernet(key)
    with open('pwd.bin', 'wb') as file:
        file.write(f.encrypt(data))


def upload_file():
    if yandex_disk:
        if any(
            file['name'] == 'pwd.bin'
            for file in yandex_disk.listdir('app:/')
        ):
            yandex_disk.remove('app:/pwd.bin')
        yandex_disk.upload('pwd.bin', 'app:/pwd.bin')


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
        print(f'login={login}, password={password}')
    except KeyError:
        print(f'Записи {serv} не найдено')


def get_base():
    print('\n'.join(passwords.keys()))


def quit():
    if base_changed:
        save_file()
        upload_file()
    exit()


funcs = {
    '1': (add_password, 'Ввести новый пароль'),
    '2': (get_password, 'Получить пароль из базы'),
    '3': (get_base, 'Получить список сервисов'),
    '4': (quit, 'Выход')
}
passwords = {}
main()
