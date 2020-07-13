# -*- coding: utf-8 -*-

import base64
import os

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from base_file import BaseFile


class Ui_MainWindow(QtWidgets.QMainWindow):

    base: BaseFile

    def __init__(self, parent, *args):
        super().__init__(*args)
        self.parent = parent
        self.base = parent.base
        self.width = 510
        self.height = 380
        self.menu_height = 20
        self.current_password = ''

        self.setObjectName("MainWindow")
        self.setFixedSize(self.width, self.height)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(5, 5, self.width - 10, self.height - 10 - self.menu_height))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.passwordsList = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.passwordsList.setObjectName("passwordsList")
        self.passwordsList.installEventFilter(self)
        self.horizontalLayout.addWidget(self.passwordsList)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.hl1 = QtWidgets.QHBoxLayout()
        self.loginTitle = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.loginView = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.hl1.addWidget(self.loginTitle)
        self.hl1.addWidget(self.loginView)

        self.verticalLayout.addLayout(self.hl1)

        self.hl2 = QtWidgets.QHBoxLayout()
        self.passTitle = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.passView = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.hl2.addWidget(self.passTitle)
        self.hl2.addWidget(self.passView)

        self.verticalLayout.addLayout(self.hl2)

        self.showButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.showButton.setObjectName("showButton")
        self.verticalLayout.addWidget(self.showButton)
        self.copyButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.copyButton.setObjectName("copyButton")
        self.verticalLayout.addWidget(self.copyButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.nameEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout.addWidget(self.nameEdit)
        self.loginEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.loginEdit.setObjectName("loginEdit")
        self.verticalLayout.addWidget(self.loginEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setMinimum(6)
        self.horizontalSlider.setMaximum(20)
        self.horizontalSlider.setProperty("value", 10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_2.addWidget(self.horizontalSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.generateButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.generateButton.setObjectName("generateButton")
        self.verticalLayout.addWidget(self.generateButton)
        self.passEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.passEdit.setObjectName("passEdit")
        self.passEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout.addWidget(self.passEdit)
        self.passEdit2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.passEdit2.setObjectName("passEdit2")
        self.passEdit2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout.addWidget(self.passEdit2)
        self.addButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, self.menu_height))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.setMenuBar(self.menubar)
        self.settings = QtWidgets.QAction(self)
        self.settings.setObjectName("settings")
        self.menu.addAction(self.settings)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.build_handlers()
        self.main_window_setup()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Менеджер паролей"))
        self.loginTitle.setText(_translate("MainWindow", "Логин"))
        self.passTitle.setText(_translate("MainWindow", "Пароль"))
        self.showButton.setText(_translate("MainWindow", "Показать пароль"))
        self.copyButton.setText(_translate("MainWindow", "Скопировать пароль"))
        self.nameEdit.setPlaceholderText(_translate("MainWindow", "Название"))
        self.loginEdit.setPlaceholderText(_translate("MainWindow", "Логин"))
        self.label.setText(_translate("MainWindow", "10"))
        self.generateButton.setText(_translate("MainWindow", "Сгенерировать случайный пароль"))
        self.passEdit.setPlaceholderText(_translate("MainWindow", "Пароль"))
        self.passEdit2.setPlaceholderText(_translate("MainWindow", "Подтверждение пароля"))
        self.addButton.setText(_translate("MainWindow", "Добавить новую запись"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.settings.setText(_translate("MainWindow", "Настройки"))

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.passwordsList:
            menu = QtWidgets.QMenu()
            menu.addAction('Удалить запись')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.remove_entry(item.text())
            return True
        return super().eventFilter(source, event)

    def main_window_setup(self):
        self.passwordsList.clear()
        self.current_password = ''
        for entry in sorted(self.base.passwords):
            self.passwordsList.addItem(entry)
        self.showButton.setEnabled(False)
        self.copyButton.setEnabled(False)
        self.addButton.setEnabled(False)
        for el in (self.loginView,
                   self.passView,
                   self.nameEdit,
                   self.loginEdit,
                   self.passEdit,
                   self.passEdit2):
            el.setText('')

    def build_handlers(self):
        self.passwordsList.itemClicked.connect(self.select_item)
        for el in (self.nameEdit, self.loginEdit, self.passEdit, self.passEdit2):
            el.textChanged.connect(self.check_all)
        self.addButton.clicked.connect(self.add_new_entry)
        self.showButton.clicked.connect(self.show_password)
        self.copyButton.clicked.connect(self.copy_password)
        self.generateButton.clicked.connect(self.generate_password)
        self.horizontalSlider.valueChanged.connect(lambda: self.label.setText(str(self.horizontalSlider.value())))

    def select_item(self):
        login, self.current_password = self.base.passwords[self.passwordsList.currentItem().text()]
        self.loginView.setText(login)
        self.passView.setText('')
        self.showButton.setEnabled(True)
        self.copyButton.setEnabled(True)

    def show_password(self):
        self.passView.setText(self.current_password)

    def copy_password(self):
        clipboard = self.parent.clipboard()
        clipboard.setText(self.current_password)

    def check_all(self):
        if all(x.text() for x in (self.nameEdit, self.loginEdit, self.passEdit, self.passEdit2)):
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

    def add_new_entry(self):
        name = self.nameEdit.text()
        login = self.loginEdit.text()
        password = self.passEdit.text()

        if name in self.base.passwords:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Изменение записи")
            mb.setText("Такая запись уже есть. Заменить?")
            button_ok = mb.addButton("Да", QtWidgets.QMessageBox.AcceptRole)
            button_cancel = mb.addButton("Нет", QtWidgets.QMessageBox.RejectRole)
            mb.exec()

            if mb.clickedButton() != button_ok:
                return

        if self.passEdit.text() != self.passEdit2.text():
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Ошибка")
            mb.setText("Пароли не совпадают")
            mb.addButton("ОК", QtWidgets.QMessageBox.AcceptRole)
            mb.exec()
            return

        if not self._check_password(password):
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Ошибка")
            mb.setText("Пароль слишком простой")
            mb.addButton("ОК", QtWidgets.QMessageBox.AcceptRole)
            mb.exec()
            return

        self.base.add_new_entry(name, login, password)
        self.main_window_setup()

    def remove_entry(self, name):
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("Удаление записи")
        mb.setText("Запись будет удалена. Вы уверены?")
        button_ok = mb.addButton("Да", QtWidgets.QMessageBox.AcceptRole)
        button_cancel = mb.addButton("Нет", QtWidgets.QMessageBox.RejectRole)
        mb.exec()

        if mb.clickedButton() != button_ok:
            return

        self.base.remove_entry(name)
        self.main_window_setup()

    def generate_password(self):
        password = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')[:self.horizontalSlider.value()]
        self.passEdit.setText(password)
        self.passEdit2.setText(password)

    @staticmethod
    def _check_password(password):
        return len(password) > 0

    def closeEvent(self, event):
        if self.base.base_changed:
            self.base.save_file()
            self.base.upload_file()
        event.accept()
