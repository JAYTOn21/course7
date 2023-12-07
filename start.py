import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from main import Ui_MainWindow
from about import aboutDialog


def aboutfun():
    dialog = aboutDialog()
    dialog.exec_()


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

    def goods_switch(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def orders_switch(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon('MR.png'))
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
