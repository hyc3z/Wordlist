# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets
import ifind_parse
import _wordlist
import time
import requests
class Ui_Dialog(object):

    def searchClicked(self):
        self.textBrowser.setText('')
        word = self.lineEdit.text()
        try:
            page_src = ifind_parse.get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index",max_retry=1)
        except requests.exceptions.RequestException:
            self.textBrowser.append('网络异常')
            return
        items = ifind_parse.parse_one_page(page_src)
        phonetics = ifind_parse.get_phonetic(page_src)
        print(phonetics)
        if items is not None and len(items):
            for i in items:
                self.textBrowser.append(i)
        else:
            self.textBrowser.append('未找到词典信息')
        if len(phonetics['us']):
            print(phonetics['us'][0])
            self.textBrowser.append('美式音标:'+phonetics['us'][0])
        if len(phonetics['uk']):
            print(phonetics['us'][0])
            self.textBrowser.append('英式音标:'+phonetics['us'][0])
        if not len(phonetics['us']) and not len(phonetics['uk']) and len(phonetics['common']):
            print(phonetics['common'][0])
            self.textBrowser.append('音标:' + phonetics['common'][0])
        if not len(phonetics['us']) and not len(phonetics['uk']) and not len(phonetics['common']):
            self.textBrowser.append('未找到音标信息')

    def initTable(self):
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['英文','中文'])
        t1 = time.time()
        wordlist = _wordlist.WordList(sqlite_dbname=os.path.join(sys.path[0], 'wordlist.db'))
        t2 = time.time()
        rows = len(wordlist)
        self.table.setRowCount(rows)
        rowcount = 0
        for i in wordlist:
            item0 = QtWidgets.QTableWidgetItem(i.it_self())
            item0.setFlags(
                QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table.setItem(rowcount,0,item0)
            item1 = QtWidgets.QTableWidgetItem(i.explanation())
            item1.setFlags(
                QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table.setItem(rowcount,1,item1)
            rowcount += 1
        t3 = time.time()
        print('Sql fetch: ',t2-t1,'Table fill: ',t3-t2)


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(318, 371)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 281, 331))
        self.tabWidget.setObjectName("tabWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(400, 400))
        self.tabWidget.setSizeIncrement(QtCore.QSize(1, 1))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table = QtWidgets.QTableWidget(self.tab_2)
        self.table.setGeometry(QtCore.QRect(10, 20, 256, 192))
        self.table.setObjectName("table")
        self.initTable()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.table, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.searchClicked)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "词库"))
        self.label.setText(_translate("Dialog", "tubao9hao@126.com"))
        self.label_2.setText(_translate("Dialog", "HycDog"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "关于"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    # hbox = QtWidgets.QHBoxLayout()
    # 设置伸缩量为1
    # hbox.addStretch(1)
    # hbox.addWidget(ui.tabWidget)
    # Dialog.setLayout(hbox)
    Dialog.show()
    sys.exit(app.exec_())
