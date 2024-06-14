from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql as mdb


def dbret():
    db = mdb.connect(host='localhost',
                     user='root',
                     password='1234',
                     database='shopdb')
    return db


class statusDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(statusDialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(562, 55)
        self.setMinimumSize(QtCore.QSize(562, 55))
        self.setMaximumSize(QtCore.QSize(562, 55))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Изменить статус заказа"))
        self.label.setText(_translate("Dialog", "Номер заказа"))
        self.pushButton.setText(_translate("Dialog", "Применить"))
        self.pushButton_2.setText(_translate("Dialog", "Отмена"))
        self.pushButton_2.clicked.connect(self.close)
        self.comboBox.addItems(["В обработке", "В пути", "Завершен"])
        self.lineEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.changeStatus)

    def changeStatus(self):
        status = self.comboBox.currentIndex() + 1
        num = self.lineEdit.text()
        db = dbret()
        cur = db.cursor()
        cur.execute(f"UPDATE shopdb.order SET orderStatus = {status} WHERE num = {num}")
        db.commit()
        db.close()
        self.close()
