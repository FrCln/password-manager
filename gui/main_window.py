# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from base_file import BaseFile


class Ui_MainWindow(QtWidgets.QMainWindow):

    base: BaseFile

    def __init__(self, base, *args):
        super().__init__(*args)
        self.base = base
        self.width = 510
        self.height = 360
        self.menu_height = 20

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
        self.horizontalLayout.addWidget(self.passwordsList)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.passView = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.passView.setObjectName("passView")
        self.verticalLayout.addWidget(self.passView)
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
        self.verticalLayout.addWidget(self.passEdit)
        self.passEdit2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.passEdit2.setObjectName("passEdit2")
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

        self.main_window_setup()
        self.build_handlers()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Менеджер паролей"))
        self.passView.setText(_translate("MainWindow", "Пароль"))
        self.showButton.setText(_translate("MainWindow", "Показать пароль"))
        self.copyButton.setText(_translate("MainWindow", "Скопировать пароль"))
        self.nameEdit.setText(_translate("MainWindow", "Название"))
        self.loginEdit.setText(_translate("MainWindow", "Логин"))
        self.label.setText(_translate("MainWindow", "10"))
        self.generateButton.setText(_translate("MainWindow", "Сгенерировать случайный пароль"))
        self.passEdit.setText(_translate("MainWindow", "Пароль"))
        self.passEdit2.setText(_translate("MainWindow", "Подтверждение пароля"))
        self.addButton.setText(_translate("MainWindow", "Добавить новую запись"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.settings.setText(_translate("MainWindow", "Настройки"))

    def main_window_setup(self):
        for entry in self.base.passwords:
            self.passwordsList.addItem(entry)
        self.showButton.setEnabled(False)
        self.copyButton.setEnabled(False)
        self.addButton.setEnabled(False)

    def build_handlers(self):
        self.passwordsList.currentItemChanged.connect(self.select_item)

    def select_item(self):
        # self.mainWindow.passwordsList.currentItem().text()
        self.showButton.setEnabled(True)
        self.copyButton.setEnabled(True)

    def closeEvent(self, event):
        if self.base.base_changed:
            self.base.save_file()
            self.base.upload_file()
        event.accept()
