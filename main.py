# -*- coding: utf-8 -*-
import os
import sys

from PyQt5 import Qt, QtWidgets

from base_file import *
from gui import mainpassword, create_new, main_window


class MainApp(Qt.QApplication):

    mainPasswordWindow: mainpassword.Ui_MainWindow
    createNewWindow: create_new.Ui_MainWindow
    mainWindow: main_window.Ui_MainWindow

    def __init__(self, *args):
        super().__init__(*args)
        self.base_changed = False
        self.base = BaseFile()
        self.connect_base()
        self.main_password = ''
        if 'pwd.bin' in os.listdir():
            self.ask_main_password()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Создание новой базы")
            mb.setText("Файл базы отсутствует. Создать новый или получить из облака?")
            button_new = mb.addButton("Создать новый", QtWidgets.QMessageBox.AcceptRole)
            button_cloud = mb.addButton("Получить из облака", QtWidgets.QMessageBox.RejectRole)
            mb.exec()

            if mb.clickedButton() == button_new:
                self.create_new_base_dialog()
            elif mb.clickedButton() == button_cloud:
                self.ask_main_password()

    def ask_main_password(self):
        self.mainPasswordWindow = mainpassword.Ui_MainWindow()
        self.mainPasswordWindow.OKButton.clicked.connect(self.enter_master_password)
        self.mainPasswordWindow.createNewButton.clicked.connect(self.cancel_master_password)
        self.mainPasswordWindow.show()

    def enter_master_password(self):
        self.main_password = self.mainPasswordWindow.passwordInput.text()
        self.mainPasswordWindow.close()
        self.read_base()

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
        self.main_password = password
        self.show_main_window()

    @staticmethod
    def _check_password(password):
        return len(password) > 0

    def connect_base(self):
        # self.base.connect_yadisk()
        self.base.check_file()

    def read_base(self):
        if self.base.status in (CLOUD_FILE_NEWER, NO_LOCAL_FILE): # CLOUD_FILE_OLDER?
            self.base.download_file()
        try:
            self.base.read_file(self.main_password)
        except FileNotFoundError:
            self.base.create_base()
        except IncorrectPassword:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Неверный пароль')
            button_ok = mb.addButton("Ввести заново", QtWidgets.QMessageBox.AcceptRole)
            button_cancel = mb.addButton("Создать новую базу", QtWidgets.QMessageBox.RejectRole)
            mb.exec()

            if mb.clickedButton() == button_ok:
                self.ask_main_password()
            elif mb.clickedButton() == button_cancel:
                self.create_new_base_dialog()
            else:
                self.quit()
        self.show_main_window()

    def show_main_window(self):
        self.mainWindow = main_window.Ui_MainWindow()
        self.main_window_setup()
        self.main_window_build_handlers()
        self.mainWindow.closeEvent = self.closeEvent
        self.mainWindow.show()

    def main_window_setup(self):
        for entry in self.base.passwords:
            self.mainWindow.passwordsList.addItem(entry)
        self.mainWindow.showButton.setEnabled(False)
        self.mainWindow.copyButton.setEnabled(False)
        self.mainWindow.addButton.setEnabled(False)

    def main_window_build_handlers(self):
        self.mainWindow.passwordsList.currentItemChanged.connect(self.select_item)

    def select_item(self):
        # self.mainWindow.passwordsList.currentItem().text()
        self.mainWindow.showButton.setEnabled(True)
        self.mainWindow.copyButton.setEnabled(True)

    def closeEvent(self, event):
        self.base.save_file()
        self.base.upload_file()
        event.accept()


def gui_exception_hook(exc_type, value, traceback):
    import traceback as tb
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(str(value))
    msg.setInformativeText('\n'.join(tb.format_exception(exc_type, value, traceback)))
    msg.setWindowTitle(exc_type.__name__)
    msg.exec_()


def main():
    app = MainApp(sys.argv)
    sys.excepthook = gui_exception_hook
    sys.exit(app.exec())



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




if __name__ == '__main__':
    main()
