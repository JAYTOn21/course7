from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pymysql as mdb

from addGoodForOrderDialog import addGFODialog


def dbret():
    db = mdb.connect(host='localhost',
                     user='root',
                     password='2173',
                     database='shopdb')
    return db

class GoodsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(GoodsTableModel, self).__init__()
        self.data = data

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return str(self.data[row][col])
        return None

    def headerData(self, p_int, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            header = ['ID', 'Производитель', 'Модель', 'Сумма']
            return header[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self, p_int, orientation, role)


class addOrderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(addOrderDialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(444, 714)
        self.setMinimumSize(QtCore.QSize(444, 714))
        self.setMaximumSize(QtCore.QSize(444, 714))
        self.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableView = QtWidgets.QTableView(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_3.addWidget(self.tableView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setMinimumSize(QtCore.QSize(90, 30))
        self.label_3.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(90, 30))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout.addWidget(self.lineEdit_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.calendarWidget = QtWidgets.QCalendarWidget(self)
        self.calendarWidget.setMinimumSize(QtCore.QSize(0, 100))
        self.calendarWidget.setMaximumSize(QtCore.QSize(16777215, 230))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.ISOWeekNumbers)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton_3.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton_4.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_4.addWidget(self.pushButton_4)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Добавление заказа"))
        self.pushButton.setText(_translate("Dialog", "Добавить"))
        self.pushButton_2.setText(_translate("Dialog", "Удалить"))
        self.label_3.setText(_translate("Dialog", "Общая сумма:"))
        self.label.setText(_translate("Dialog", "Номер заказа"))
        self.label_2.setText(_translate("Dialog", "Номер телефона заказчика"))
        self.pushButton_3.setText(_translate("Dialog", "Добавить"))
        self.pushButton_4.setText(_translate("Dialog", "Отмена"))
        self.pushButton_4.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.addGoodForOrder)
        self.data = ()

    def addGoodForOrder(self):
        add = addGFODialog()
        add.exec_()
        ind, count = 0, 0
        if add.pushButton.text() == "+":
            ind = str(add.tableView.model().index(add.tableView.currentIndex().row(), 0).data())
            count = add.spinbox.value()
        if ind != 0:
            if self.data == ():
                db = dbret()
                cur = db.cursor()
                cur.execute(f'select idgoods, manufacturers.name, model, (price * {count}) from goods, manufacturers '
                            f'where idgoods = {ind} and manufacturers_idmanufacturers = manufacturers.idmanufacturers')
                self.data = cur.fetchall()
                model = GoodsTableModel(self.data)



