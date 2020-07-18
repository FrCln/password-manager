# -*- coding: utf-8 -*-
import os
import sys

from PyQt5 import Qt, QtWidgets, QtCore

from base_file import *
from gui import main_password, create_new_base, main_window


class MainApp(Qt.QApplication):

    mainPasswordWindow: main_password.Ui_MainWindow
    createNewWindow: create_new_base.Ui_MainWindow
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

    def connect_base(self):
        try:
            self.base.connect_yadisk()
        except UserCancelException:
            sys.exit(0)
        self.base.check_file()

    def ask_main_password(self):
        self.mainPasswordWindow = main_password.Ui_MainWindow(self)
        self.mainPasswordWindow.send_password_signal.connect(self.read_base)
        self.mainPasswordWindow.create_new_signal.connect(self.create_new_base_dialog)
        self.mainPasswordWindow.show()

    @QtCore.pyqtSlot()
    def create_new_base_dialog(self):
        self.createNewWindow = create_new_base.Ui_MainWindow(self)
        self.createNewWindow.create_new_ok.connect(self.show_main_window)
        self.createNewWindow.show()

    @QtCore.pyqtSlot()
    def read_base(self):
        if self.base.status in (CLOUD_FILE_NEWER, NO_LOCAL_FILE): # CLOUD_FILE_OLDER?
            self.base.download_file()
        try:
            self.base.main_password = self.main_password
            self.base.read_file()
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

    @QtCore.pyqtSlot()
    def show_main_window(self):
        self.mainWindow = main_window.Ui_MainWindow(self)
        self.mainWindow.show()


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


if __name__ == '__main__':
    main()
