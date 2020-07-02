import base64
import json
import os
import webbrowser
from datetime import datetime, timezone
from typing import Optional

import yadisk
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

NO_YANDEX_DISK = 0
NO_FILE_IN_CLOUD = 1
CLOUD_FILE_OLDER = 2
CLOUD_FILE_NEWER = 3
FILES_IDENTICAL = 4
NO_LOCAL_FILE = 5


class IncorrectPassword(Exception):
    pass


class FileCorrupted(Exception):
    pass


class BaseFile:
    yandex_disk: Optional[yadisk.YaDisk]
    passwords: dict

    def __init__(self):
        self.yandex_disk = None
        self.passwords = {}
        self.generate_salt()

    def generate_salt(self):
        self.salt = b'\x82\xe1\x85~!\xaf\xd5\xd2}\xbc#\xf0\x0f\xed\x02\xf9'

    def connect_yadisk(self):
        try:
            with open('yadisk-secret.txt') as f:
                application_id = f.readline().strip()
                application_secret = f.readline().strip()
                yadisk_token = f.readline().strip()

        except FileNotFoundError:
            print('Яндекс-диск недоступен')
            return

        if not yadisk_token:
            self.yandex_disk = yadisk.YaDisk(application_id, application_secret)
            url = self.yandex_disk.get_code_url()
            webbrowser.open(url)
            code = input('Введите код, полученный от Яндекс-диска: ')
            try:
                response = self.yandex_disk.get_token(code)
            except yadisk.exceptions.BadRequestError:
                print("Bad code")
                sys.exit(1)

            yadisk_token = self.yandex_disk.token = response.access_token
            with open('yadisk-secret.txt', 'a') as f:
                f.write('\n' + yadisk_token + '\n')

        else:
            self.yandex_disk = yadisk.YaDisk(token=yadisk_token)

        if not yandex_disk.check_token():
            print('Яндекс-диск недоступен')
            self.yandex_disk = None

    def check_file(self):
        if not self.yandex_disk:
            return NO_YANDEX_DISK

        for file in self.yandex_disk.listdir('app:/'):
            if file['name'] == 'pwd.bin':
                created = file['created']
                break
        else:
            return NO_FILE_IN_CLOUD

        try:
            local_file_date = datetime.fromtimestamp(
                os.path.getmtime('pwd.bin'), timezone.utc
            )
        except FileNotFoundError:
            return NO_LOCAL_FILE

        if created < local_file_date:
            return CLOUD_FILE_OLDER
        elif created > local_file_date:
            return CLOUD_FILE_NEWER
        else:
            return FILES_IDENTICAL

    def download_file(self):
        self.yandex_disk.download('app:/pwd.bin', 'pwd.bin')

    def read_file(self, main_password):
        self.main_password = main_password
        try:
            with open('pwd.bin', 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            raise
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.main_password.encode(encoding='utf-8')))
        f = Fernet(key)
        try:
            data = f.decrypt(data)
        except InvalidToken:
            raise IncorrectPassword
        try:
            self.passwords = json.loads(data)
        except ValueError:
            raise FileCorrupted

    def save_file(self):
        data = json.dumps(self.passwords).encode(encoding='utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.main_password.encode(encoding='utf-8')))
        f = Fernet(key)
        with open('pwd.bin', 'wb') as file:
            file.write(f.encrypt(data))

    def upload_file(self):
        if self.yandex_disk:
            if any(
                    file['name'] == 'pwd.bin'
                    for file in self.yandex_disk.listdir('app:/')
            ):
                self.yandex_disk.remove('app:/pwd.bin')
            self.yandex_disk.upload('pwd.bin', 'app:/pwd.bin')

    def create_base(self):
        self.passwords = {}
