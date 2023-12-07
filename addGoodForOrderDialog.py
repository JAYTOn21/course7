from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql as mdb
from PyQt5.QtCore import Qt


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
            header = ['ID', 'Категория', 'Производитель', 'Модель', 'Цена', 'Количество', 'Оценка', 'Вес', 'x', 'y',
                      'z', 'Категория', 'Производитель']
            return header[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self, p_int, orientation, role)


class addGFODialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(addGFODialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(521, 435)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self)
        self.comboBox_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_2.addWidget(self.comboBox_2)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinbox = QtWidgets.QSpinBox(self)
        self.spinbox.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinbox.setFont(font)
        self.spinbox.setObjectName("spinbox")
        self.spinbox.setMaximum(9999999)
        self.horizontalLayout.addWidget(self.spinbox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.loaddata()
        db = dbret()
        cur = db.cursor()
        self.comboBox.clear()
        self.comboBox_2.clear()
        cur.execute('select name from categories')
        data = cur.fetchall()
        self.comboBox.addItem("Категории")
        for i in range(len(data)):
            self.comboBox.addItem(str(data[i][0]))
        cur.execute("select name from manufacturers")
        data = cur.fetchall()
        self.comboBox_2.addItem("Производители")
        for i in range(len(data)):
            self.comboBox_2.addItem(str(data[i][0]))
        db.close()
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Добавление товара в заказ"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Поиск товара"))
        self.label.setText(_translate("Dialog", "Количество:"))
        self.pushButton.setText(_translate("Dialog", "Добавить"))
        self.pushButton_2.setText(_translate("Dialog", "Отмена"))
        self.pushButton_2.clicked.connect(self.close)
        self.lineEdit.textChanged.connect(self.goodsfilterdata)
        self.comboBox.currentIndexChanged.connect(self.goodsfilterdata)
        self.comboBox_2.currentIndexChanged.connect(self.goodsfilterdata)
        self.pushButton.clicked.connect(self.add)

    def add(self):
        self.pushButton.setText("+")
        self.close()

    def loaddata(self):
        db = dbret()
        cur = db.cursor()
        cur.execute("SELECT idgoods, categories.name, manufacturers.name, model, price, count, opinion, weight, x, "
                    "y, z  FROM shopdb.goods, shopdb.categories, shopdb.manufacturers where categories_idcategories = "
                    "idcategories and manufacturers_idmanufacturers = idmanufacturers order by idgoods;")
        data = cur.fetchall()
        if data == ():
            data = (('', '', '', '', '', '', '', '', '', ''),)
        model = GoodsTableModel(data)
        self.tableView.setModel(model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.resizeColumnsToContents()
        self.tableView.setSelectionMode(self.tableView.SingleSelection)
        db.close()

    def goodsfilterdata(self):
        db = dbret()
        cur = db.cursor()
        txt = self.lineEdit.text()
        cur.execute(f"select idgoods from goods where model like '%{txt}%'")
        ids = cur.fetchall()
        str1 = "("
        for i in range(len(ids)):
            if i != len(ids) - 1:
                str1 = str1 + str(ids[i][0]) + ", "
            else:
                str1 = str1 + str(ids[i][0]) + ")"
        if str1 != "(":
            if self.comboBox.currentIndex() != 0 and self.comboBox_2.currentIndex() != 0:
                cur.execute(
                    f"SELECT idgoods, categories.name, manufacturers.name, model, price, count, opinion, weight, x,"
                    f" y, z  FROM shopdb.goods, shopdb.categories, shopdb.manufacturers where "
                    f"categories_idcategories = idcategories and manufacturers_idmanufacturers = idmanufacturers "
                    f"and categories.name = '{str(self.comboBox.currentText())}' and manufacturers.name = "
                    f"'{str(self.comboBox_2.currentText())}' and idgoods in {str1};")
                data = cur.fetchall()
            elif self.comboBox.currentIndex() != 0:
                cur.execute(
                    f"SELECT idgoods, categories.name, manufacturers.name, model, price, count, opinion, weight, x,"
                    f" y, z  FROM shopdb.goods, shopdb.categories, shopdb.manufacturers where "
                    f"categories_idcategories = idcategories and manufacturers_idmanufacturers = idmanufacturers "
                    f"and categories.name = '{str(self.comboBox.currentText())}' and idgoods in {str1};")
                data = cur.fetchall()
            elif self.comboBox_2.currentIndex() != 0:
                cur.execute(
                    f"SELECT idgoods, categories.name, manufacturers.name, model, price, count, opinion, weight, x,"
                    f" y, z  FROM shopdb.goods, shopdb.categories, shopdb.manufacturers where "
                    f"categories_idcategories = idcategories and manufacturers_idmanufacturers = idmanufacturers "
                    f"and manufacturers.name = '{str(self.comboBox_2.currentText())}' and idgoods in {str1};")
                data = cur.fetchall()
            elif txt != "":
                cur.execute(f"SELECT idgoods, categories.name, manufacturers.name, model, price, count, opinion, "
                            f"weight, x, y, z  FROM shopdb.goods, shopdb.categories, shopdb.manufacturers where "
                            f"categories_idcategories = idcategories and manufacturers_idmanufacturers = "
                            f"idmanufacturers and idgoods in {str1};")
                data = cur.fetchall()
            else:
                data = (1,)
        else:
            data = ()
        if data == (1,):
            self.loaddata()
        elif data != ():
            model = GoodsTableModel(data)
            self.tableView.setModel(model)
            self.tableView.setColumnHidden(0, True)
            self.tableView.resizeColumnsToContents()
        else:
            data = (('', '', '', '', '', '', '', '', '', '', ''),)
            model = GoodsTableModel(data)
            self.tableView.setModel(model)
            self.tableView.setColumnHidden(0, True)
            self.tableView.resizeColumnsToContents()
        db.close()