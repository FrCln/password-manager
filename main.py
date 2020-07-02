# -*- coding: utf-8 -*-
import os
import sys

from PyQt5 import Qt, QtWidgets

from base_file import *
from gui import mainpassword, create_new


class MainApp(Qt.QApplication):

    mainPasswordWindow: mainpassword.Ui_MainWindow
    createNewWindow: create_new.Ui_MainWindow

    def __init__(self, *args):
        super().__init__(*args)
        self.base_changed = False
        self.base = BaseFile()
        self.main_password = ''
        if 'pwd.bin' in os.listdir():
            self.ask_main_password()
        else:
            # dialog yaDisk
            self.create_new_base_dialog()

    def ask_main_password(self):
        self.mainPasswordWindow = mainpassword.Ui_MainWindow()
        self.mainPasswordWindow.OKButton.clicked.connect(self.enter_master_password)
        self.mainPasswordWindow.createNewButton.clicked.connect(self.cancel_master_password)
        self.mainPasswordWindow.show()

    def enter_master_password(self):
        self.main_password = self.mainPasswordWindow.passwordInput.text()
        self.mainPasswordWindow.close()
        print(self.main_password) # FIXIT

    def cancel_master_password(self):
        if 'pwd.bin' in os.listdir():
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Создание новой базы")
            mb.setText("Имеющаяся база будет удалена! Вы уверены?")
            button_ok = mb.addButton("Да", QtWidgets.QMessageBox.AcceptRole)
            button_cancel = mb.addButton("Нет", QtWidgets.QMessageBox.RejectRole)
            mb.exec()

            if mb.clickedButton() == button_ok:
                self.mainPasswordWindow.close()
                self.create_new_base_dialog()

    def create_new_base_dialog(self):
        self.createNewWindow = create_new.Ui_MainWindow()
        self.createNewWindow.OKButton.clicked.connect(self.create_new_base_ok)
        self.createNewWindow.show()

    def create_new_base_ok(self):
        if self.createNewWindow.lineEdit.text() != self.createNewWindow.lineEdit_2.text():
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Ошибка")
            mb.setText("Пароли не совпадают")
            mb.addButton("ОК", QtWidgets.QMessageBox.AcceptRole)
            mb.exec()
            return
        password = self.createNewWindow.lineEdit.text()
        if not self._check_password(password):
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Ошибка")
            mb.setText("Пароль слишком простой")
            mb.addButton("ОК", QtWidgets.QMessageBox.AcceptRole)
            mb.exec()
            return
        self.createNewWindow.close()
        self.create_new_base(password)

    @staticmethod
    def _check_password(password):
        return len(password) > 0

    def create_new_base(self, password):
        print(password) # FIXIT


def main():
    app = MainApp(sys.argv)
    sys.exit(app.exec())


def old_main():
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
