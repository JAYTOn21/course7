from PyQt5 import QtCore, QtGui, QtWidgets


class aboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(aboutDialog, self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(334, 256)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setMinimumSize(QtCore.QSize(316, 200))
        self.textBrowser.setMaximumSize(QtCore.QSize(316, 200))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBrowser.setPalette(palette)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "О программе"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Программное обеспечение для работы с базой данных для интернет-магазина.<br />Реализовано с помощью MySQL и PyQt5.<br />Разработчик: Акинин А.А.<br />Абакан, 2023</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Закрыть"))
        self.pushButton.clicked.connect(self.close)

