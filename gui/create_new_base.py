# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create-new.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    create_new_ok = QtCore.pyqtSignal()

    def __init__(self, parent, *args):
        super().__init__(*args)
        self.parent = parent
        self.setObjectName("MainWindow")
        self.resize(298, 119)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 281, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_0 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_0.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_0)

        self.lineEdit_0 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_0.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_0)

        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)

        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.OKButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.OKButton.setObjectName("pushButton_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.OKButton)

        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.build_handlers()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Новая база"))
        self.label_0.setText(_translate("MainWindow", "Имя файла:"))
        self.label.setText(_translate("MainWindow", "Введите пароль:"))
        self.label_2.setText(_translate("MainWindow", "Еще раз:"))
        self.OKButton.setText(_translate("MainWindow", "ОК"))
        self.lineEdit_0.setText('pwd.bin')

    def build_handlers(self):
        self.OKButton.clicked.connect(self.create_new_base_ok)

    def create_new_base_ok(self):
        if self.lineEdit.text() != self.lineEdit_2.text():
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Ошибка")
            mb.setText("Пароли не совпадают")
            mb.addButton("ОК", QtWidgets.QMessageBox.AcceptRole)
            mb.exec()
            return
        password = self.lineEdit.text()
        if not self._check_password(password):
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle("Ошибка")
            mb.setText("Пароль слишком простой")
            mb.addButton("ОК", QtWidgets.QMessageBox.AcceptRole)
            mb.exec()
            return
        self.parent.settings.filename = self.lineEdit_0.text()
        self.parent.main_password = password
        self.create_new_ok.emit()
        self.close()

    @staticmethod
    def _check_password(password):
        return len(password) > 0
