from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pymysql as mdb
from addGood import addGoodDialog
from addOrder import addOrderDialog


def dbret():
    db = mdb.connect(host='localhost',
                     user='root',
                     password='1234',
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
            header = ['ID', 'Артикул', 'Категория', 'Производитель', 'Модель', 'Цена', 'Количество', 'Оценка']
            return header[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self, p_int, orientation, role)


class OrdersTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(OrdersTableModel, self).__init__()
        self.data = data

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            if col == 4:
                if str(self.data[row][col]) == '1':
                    return "В обработке"
                elif str(self.data[row][col]) == '2':
                    return "В пути"
                else:
                    return "Завершен"
            else:
                return str(self.data[row][col])
        return None

    def headerData(self, p_int, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            header = ['Номер заказа', 'Сумма', 'Дата', 'Номер телефона', 'Статус заказа']
            return header[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self, p_int, orientation, role)


class OrdersListTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(OrdersListTableModel, self).__init__()
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
            header = ['Производитель', 'Модель', 'Количество', 'Сумма']
            return header[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self, p_int, orientation, role)


class Ui_MainWindow(object):
    def loaddata(self):
        db = dbret()
        cur = db.cursor()
        cur.execute("SELECT idgoods, articul, categories.name, manufacturers.name, model, price, count, opinion FROM "
                    "shopdb.goods, shopdb.categories, shopdb.manufacturers where categories_idcategories ="
                    "idcategories and manufacturers_idmanufacturers = idmanufacturers order by idgoods;")
        data = cur.fetchall()
        if data == ():
            data = (('', '', '', '', '', '', ''),)
        model = GoodsTableModel(data)
        self.tableView.setModel(model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.resizeColumnsToContents()
        self.tableView.setSelectionMode(self.tableView.SingleSelection)
        cur.execute('SELECT distinct num, allsum, order.date, (select email from auth_user where id = user_iduser), '
                    'orderStatus FROM shopdb.order;')
        data = cur.fetchall()
        if data == ():
            data = (('', '', '', '', ''),)
        model = OrdersTableModel(data)
        self.tableView_2.setModel(model)
        self.tableView_2.resizeColumnsToContents()
        self.tableView_2.setSelectionMode(self.tableView_2.SingleSelection)
        db.close()

    def orderlistdata(self):
        ind = self.tableView_2.model().index(self.tableView_2.currentIndex().row(), 0).data()
        if ind != "":
            db = dbret()
            cur = db.cursor()
            cur.execute(f'SELECT manufacturers.name, goods.model, order.count, sum FROM shopdb.order, shopdb.goods, '
                        f'shopdb.manufacturers where goods_idgoods = goods.idgoods and '
                        f'goods.manufacturers_idmanufacturers = manufacturers.idmanufacturers and num = {ind};')
            data = cur.fetchall()
            if data == ():
                data = (('', '', '', ''),)
            model = OrdersListTableModel(data)
            self.tableView_3.setModel(model)
            self.tableView_3.resizeColumnsToContents()
            self.tableView_3.setSelectionMode(self.tableView_3.SingleSelection)

    def delGoodFun(self):
        ind = str(self.tableView.model().index(self.tableView.currentIndex().row(), 0).data())
        db = dbret()
        cur = db.cursor()
        cur.execute(f"select distinct num from shopdb.order where goods_idgoods = {ind}")
        numNeed = cur.fetchall()
        if numNeed != ():
            num = numNeed[0][0]
            sql = "DELETE FROM shopdb.order WHERE num = %s"
            val = (num,)
            cur.execute(sql, val)
            db.commit()
        print(1)
        sql = "DELETE FROM goods WHERE idgoods = %s"
        val = (ind,)
        cur.execute(sql, val)
        db.commit()
        db.close()

    def delOrderFun(self):
        num = str(self.tableView_2.model().index(self.tableView_2.currentIndex().row(), 0).data())
        db = dbret()
        cur = db.cursor()
        sql = "DELETE FROM shopdb.order WHERE num = %s"
        val = (num,)
        cur.execute(sql, val)
        db.commit()
        db.close()
        self.orderlistdata()

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
                    f"SELECT idgoods, articul, categories.name, manufacturers.name, model, price, count, opinion FROM "
                    f"shopdb.goods, shopdb.categories, shopdb.manufacturers where categories_idcategories = "
                    f"idcategories and manufacturers_idmanufacturers = idmanufacturers and categories.name = "
                    f"'{str(self.comboBox.currentText())}' and manufacturers.name = "
                    f"'{str(self.comboBox_2.currentText())}' and idgoods in {str1};")
                data = cur.fetchall()
            elif self.comboBox.currentIndex() != 0:
                cur.execute(
                    f"SELECT idgoods, articul, categories.name, manufacturers.name, model, price, count, opinion FROM "
                    f"shopdb.goods, shopdb.categories, shopdb.manufacturers where categories_idcategories = "
                    f"idcategories and manufacturers_idmanufacturers = idmanufacturers and categories.name = "
                    f"'{str(self.comboBox.currentText())}' and idgoods in {str1};")
                data = cur.fetchall()
            elif self.comboBox_2.currentIndex() != 0:
                cur.execute(
                    f"SELECT idgoods, articul, categories.name, manufacturers.name, model, price, count, opinion FROM "
                    f"shopdb.goods, shopdb.categories, shopdb.manufacturers where "
                    f"categories_idcategories = idcategories and manufacturers_idmanufacturers = idmanufacturers "
                    f"and manufacturers.name = '{str(self.comboBox_2.currentText())}' and idgoods in {str1};")
                data = cur.fetchall()
            elif txt != "":
                cur.execute(f"SELECT idgoods, articul, categories.name, manufacturers.name, model, price, count, "
                            f"opinion FROM shopdb.goods, shopdb.categories, shopdb.manufacturers where "
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
            data = (('', '', '', '', '', '', ''),)
            model = GoodsTableModel(data)
            self.tableView.setModel(model)
            self.tableView.setColumnHidden(0, True)
            self.tableView.resizeColumnsToContents()
        db.close()

    def searchorder(self):
        txt = self.lineEdit_2.text()
        if txt != "":
            db = dbret()
            cur = db.cursor()
            cur.execute(
                f"SELECT distinct num, allsum, order.date, (select email from auth_user where id = user_iduser), "
                f"orderStatus FROM shopdb.order where num like ('%' + '{txt}' + '%');")
            data = cur.fetchall()
            if data == ():
                data = (('', '', '', '', ''),)
            model = OrdersTableModel(data)
            self.tableView_2.setModel(model)
            self.tableView_2.resizeColumnsToContents()
            self.tableView_2.setSelectionMode(self.tableView_2.SingleSelection)
        else:
            self.loaddata()

    def addChoice(self):
        if self.stackedWidget.currentWidget() == self.page:
            add = addGoodDialog()
            add.exec_()
        else:
            add = addOrderDialog()
            add.exec_()
        self.loaddata()
        self.filtersUpdate()

    def filtersUpdate(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        db = dbret()
        cur = db.cursor()
        cur.execute("select name from categories order by name")
        data = cur.fetchall()
        self.comboBox.addItem("Категории")
        for i in range(len(data)):
            self.comboBox.addItem(str(data[i][0]))
        cur.execute("select name from manufacturers order by name")
        data = cur.fetchall()
        self.comboBox_2.addItem("Производители")
        for i in range(len(data)):
            self.comboBox_2.addItem(str(data[i][0]))
        db.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout = QtWidgets.QGridLayout(self.page)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.page)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.page)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.page)
        self.comboBox_2.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_2.addWidget(self.comboBox_2)
        self.lineEdit = QtWidgets.QLineEdit(self.page)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView_2 = QtWidgets.QTableView(self.page_2)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout_2.addWidget(self.tableView_2, 1, 0, 1, 1)
        self.tableView_3 = QtWidgets.QTableView(self.page_2)
        self.tableView_3.setObjectName("tableView_3")
        self.gridLayout_2.addWidget(self.tableView_3, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout_3.addWidget(self.stackedWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_card = QtWidgets.QAction(MainWindow)
        self.action_card.setObjectName("action_card")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.actionStatus = QtWidgets.QAction(MainWindow)
        self.actionStatus.setObjectName("actionStatus")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu_2.addAction(self.action_card)
        self.menu_2.addAction(self.action_4)
        self.menu_2.addAction(self.actionStatus)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.filtersUpdate()
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "База данных"))
        self.pushButton.setText(_translate("MainWindow", "Товары"))
        self.pushButton_2.setText(_translate("MainWindow", "Заказы"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Поиск товара по модели"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Поиск заказа по номеру"))
        self.menu.setTitle(_translate("MainWindow", "Данные"))
        self.menu_2.setTitle(_translate("MainWindow", "Информация"))
        self.action.setText(_translate("MainWindow", "Добавить"))
        self.action_2.setText(_translate("MainWindow", "Изменить"))
        self.action_3.setText(_translate("MainWindow", "Удалить"))
        self.action_card.setText(_translate("MainWindow", "О товаре"))
        self.action_4.setText(_translate("MainWindow", "О программе"))
        self.actionStatus.setText(_translate("MainWindow", "Изменить статус заказа"))
