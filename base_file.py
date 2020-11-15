import base64
import json
import os
import webbrowser
from datetime import datetime, timezone
from typing import Optional

from PyQt5 import QtWidgets
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


class UserCancelException(Exception):
    pass


class BaseFile(QtWidgets.QWidget):

    yandex_disk: Optional[yadisk.YaDisk]
    status: int
    base_changed: bool

    def __init__(self, *args):
        super().__init__(*args)
        self.yandex_disk = None
        self.main_password = ''
        self._passwords = {}
        self.status = 0
        self.base_changed = False
        self.generate_salt()

    def generate_salt(self):
        self.salt = b'\x82\xe1\x85~!\xaf\xd5\xd2}\xbc#\xf0\x0f\xed\x02\xf9'

    @property
    def passwords(self):
        return self._passwords

    def connect_cloud(self):
        try:
            with open('yadisk-token.txt') as f:
                yadisk_token = f.readline().strip()
        except FileNotFoundError:
            self.get_new_token()
            return

        self.yandex_disk = yadisk.YaDisk(token=yadisk_token)
        if not self.yandex_disk.check_token():
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Ошибка')
            mb.setText('Токен Яндекс-диска некорректен.\nПолучить новый?')
            ok = mb.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
            cancel = mb.addButton('Отмена', QtWidgets.QMessageBox.RejectRole)
            mb.exec()

            if mb.clickedButton() == ok:
                self.get_new_token()
            else:
                self.yadisk_error_dialog()

    def get_new_token(self):
        try:
            with open('yadisk-secret.txt') as f:
                application_id = f.readline().strip()
                application_secret = f.readline().strip()
        except FileNotFoundError:
            self.yadisk_error_dialog('Данные Yandex OAuth не найдены. '
                                     'Чтобы зарегистрировать приложение, '
                                     'перейдите по адресу: https://oauth.yandex.ru '
                                     'и сохраните выданные id и пароль в файл '
                                     'yadisk-secret.txt')
            return

        self.yandex_disk = yadisk.YaDisk(application_id, application_secret)
        url = self.yandex_disk.get_code_url()
        webbrowser.open(url)
        while True:
            code, ok = QtWidgets.QInputDialog.getText(
                self,
                'Подтверждение',
                'Введите код подтверждения, полученный от Яндекс-диска:'
            )
            if ok:
                try:
                    response = self.yandex_disk.get_token(code)
                    break
                except yadisk.exceptions.BadRequestError:
                    mb = QtWidgets.QMessageBox()
                    mb.setWindowTitle('Ошибка')
                    mb.setText('Неверный код.')
                    ok = mb.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
                    mb.exec()

                    if mb.clickedButton() == ok:
                        continue
                    else:
                        self.yadisk_error_dialog()
                        return

        yadisk_token = self.yandex_disk.token = response.access_token
        with open('yadisk-token.txt', 'w') as f:
            f.write(yadisk_token)

    def yadisk_error_dialog(self, msg=None):
        msg = msg or 'Яндекс-диск недоступен.'
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle('Ошибка')
        mb.setText(msg + '\nРаботать оффлайн?')
        ok = mb.addButton('OK', QtWidgets.QMessageBox.AcceptRole)
        cancel = mb.addButton('Отмена', QtWidgets.QMessageBox.RejectRole)
        mb.exec()

        if mb.clickedButton() == ok:
            self.yandex_disk = None
        else:
            raise UserCancelException

    def check_file(self):
        if not self.yandex_disk:
            self.status = NO_YANDEX_DISK
            return

        for file in self.yandex_disk.listdir('app:/'):
            if file['name'] == 'pwd.bin':
                created = file['created']
                break
        else:
            self.status = NO_FILE_IN_CLOUD
            return

        try:
            local_file_date = datetime.fromtimestamp(
                os.path.getmtime('pwd.bin'), timezone.utc
            )
        except FileNotFoundError:
            self.status = NO_LOCAL_FILE
            return

        if created < local_file_date:
            self.status = CLOUD_FILE_OLDER
        elif created > local_file_date:
            self.status = CLOUD_FILE_NEWER
        else:
            self.status = FILES_IDENTICAL

    def download_file(self):
        self.yandex_disk.download('app:/pwd.bin', 'pwd.bin')

    def read_file(self):
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
            self._passwords = json.loads(data)
        except ValueError:
            raise FileCorrupted

    def add_new_entry(self, name, login, password):
        self._passwords[name] = (login, password)
        self.base_changed = True

    def remove_entry(self, name):
        self._passwords.pop(name)
        self.base_changed = True

    def save_file(self):
        data = json.dumps(self._passwords).encode(encoding='utf-8')
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
        self._passwords = {}
