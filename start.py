import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from main import Ui_MainWindow
from about import aboutDialog
from card import cardDialog
from status import statusDialog


def aboutfun():
    dialog = aboutDialog()
    dialog.exec_()


def delGoodDialog():
    dlg = QMessageBox()
    dlg.setWindowTitle("Удаление товара")
    dlg.setText("Вы уверены, что хотите удалить этот товар?\nВсе заказы, в которых содержится этот товар, также будут "
                "удалены.")
    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    but1 = dlg.button(QMessageBox.Yes)
    but1.setText("Да")
    but2 = dlg.button(QMessageBox.No)
    but2.setText("Нет")
    dlg.setIcon(QMessageBox.Question)
    dlg.exec()
    if dlg.clickedButton() == but1:
        return 1
    else:
        return 2


def delOrderDialog():
    dlg = QMessageBox()
    dlg.setWindowTitle("Удаление заказа")
    dlg.setText("Вы уверены, что хотите удалить этот заказ?")
    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    but1 = dlg.button(QMessageBox.Yes)
    but1.setText("Да")
    but2 = dlg.button(QMessageBox.No)
    but2.setText("Нет")
    dlg.setIcon(QMessageBox.Question)
    dlg.exec()
    if dlg.clickedButton() == but1:
        return 1
    else:
        return 2


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.pushButton.clicked.connect(self.goods_switch)
        self.ui.pushButton_2.clicked.connect(self.orders_switch)
        self.ui.loaddata()
        self.ui.tableView_2.clicked.connect(self.ui.orderlistdata)
        self.ui.lineEdit_2.textChanged.connect(self.ui.searchorder)
        self.ui.lineEdit.textChanged.connect(self.ui.goodsfilterdata)
        self.ui.comboBox.currentIndexChanged.connect(self.ui.goodsfilterdata)
        self.ui.comboBox_2.currentIndexChanged.connect(self.ui.goodsfilterdata)
        self.ui.action_4.triggered.connect(aboutfun)
        self.ui.action.triggered.connect(self.ui.addChoice)
        self.ui.action_3.triggered.connect(self.delGoodFun)
        self.ui.action_card.triggered.connect(self.showCard)
        self.ui.actionStatus.triggered.connect(self.changeStatusOrder)

    def goods_switch(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def delGoodFun(self):
        if self.ui.stackedWidget.currentWidget() == self.ui.page:
            ind = str(self.ui.tableView.model().index(self.ui.tableView.currentIndex().row(), 0).data())
            if ind is not None:
                data = delGoodDialog()
                if data == 1:
                    self.ui.delGoodFun()
                    self.ui.loaddata()
        else:
            ind = str(self.ui.tableView_2.model().index(self.ui.tableView_2.currentIndex().row(), 0).data())
            if ind is not None:
                data = delOrderDialog()
                if data == 1:
                    self.ui.delOrderFun()
                    self.ui.loaddata()

    def orders_switch(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def showCard(self):
        if self.ui.stackedWidget.currentWidget() == self.ui.page:
            ind = str(self.ui.tableView.model().index(self.ui.tableView.currentIndex().row(), 0).data())
            card = cardDialog()
            card.label_12.setText(ind)
            card.loaddata()
            card.exec_()

    def changeStatusOrder(self):
        ind = str(self.ui.tableView_2.model().index(self.ui.tableView_2.currentIndex().row(), 0).data())
        if self.ui.stackedWidget.currentWidget() == self.ui.page_2 and ind != "None":
            statusDiag = statusDialog()
            statusDiag.lineEdit.setText(self.ui.tableView_2.model().index(self.ui.tableView_2.currentIndex().row(), 0).data())
            curStatus = self.ui.tableView_2.model().index(self.ui.tableView_2.currentIndex().row(), 4).data()
            if curStatus == "В обработке":
                statusDiag.comboBox.setCurrentIndex(0)
            elif curStatus == "В пути":
                statusDiag.comboBox.setCurrentIndex(1)
            else:
                statusDiag.comboBox.setCurrentIndex(2)
            statusDiag.exec_()
            self.ui.loaddata()


    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('MR.png'))
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
