# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first.ui'
#
# Created by: Gui UI code generator 5.13.0
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
        self.pushButton_2.setEnabled(False)
        self.textBrowser.setText('')
        word = self.lineEdit.text()
        explain_db = self.wordlist.search_sqlite(word)
        if len(explain_db):
            self.textBrowser.append('已于'+explain_db[1]+'录入数据库')
            self.textBrowser.append(explain_db[0])
        else:
            try:
                page_src = ifind_parse.get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index",max_retry=1)
            except requests.exceptions.RequestException:
                self.textBrowser.append('网络异常')
                return
            self.items = ifind_parse.parse_one_page(page_src)
            self.phonetics = ifind_parse.get_phonetic(page_src)
            self.last_search = word
            print(self.phonetics)
            if self.items is not None and len(self.items):
                for i in self.items:
                    self.textBrowser.append(i)
                self.pushButton_2.setEnabled(True)
            else:
                self.textBrowser.append('未找到词典信息')
            if len(self.phonetics['us']):
                print(self.phonetics['us'][0])
                self.textBrowser.append('美式音标:'+self.phonetics['us'][0])
            if len(self.phonetics['uk']):
                print(self.phonetics['us'][0])
                self.textBrowser.append('英式音标:'+self.phonetics['us'][0])
            if not len(self.phonetics['us']) and not len(self.phonetics['uk']) and len(self.phonetics['common']):
                print(self.phonetics['common'][0])
                self.textBrowser.append('音标:' + self.phonetics['common'][0])
            if not len(self.phonetics['us']) and not len(self.phonetics['uk']) and not len(self.phonetics['common']):
                self.textBrowser.append('未找到音标信息')

    def addClicked(self):
        self.pushButton_2.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.pushButton.setEnabled(False)
        str = ''
        for i in self.items:
            str += i
        retmsg = self.wordlist.add_new_word(self.last_search,str)
        self.textBrowser.append('-----------')
        for i in retmsg:
            self.textBrowser.append(i)
        self.initTable()
        self.pushButton.setEnabled(True)
        self.lineEdit.setEnabled(True)


    def initTable(self):
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['英文','中文'])
        t1 = time.time()
        self.wordlist = _wordlist.WordList(sqlite_dbname=os.path.join(sys.path[0], 'wordlist.db'))
        self.wordlist.sort_by_alphabet()
        t2 = time.time()
        rows = len(self.wordlist)
        self.table.setRowCount(rows)
        rowcount = 0
        for i in self.wordlist:
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

    def refreshClicked(self):
        self.pushButton_3.setEnabled(False)
        self.initTable()
        self.pushButton_3.setEnabled(True)

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
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 2, 0, 1, 1)
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
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 2, 0, 1, 1)
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
        self.pushButton_2.clicked.connect(self.addClicked)
        self.pushButton_3.clicked.connect(self.refreshClicked)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "iFindWord v1.0.1"))
        self.pushButton.setText(_translate("Dialog", "搜索"))
        self.pushButton_2.setText(_translate("Dialog", "添加到词库"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "词库"))
        self.pushButton_3.setText(_translate("Dialog", "刷新"))
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
