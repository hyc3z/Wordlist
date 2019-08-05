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

    def search(self):
        word = self.lineEdit_2.text()
        self.getWordlist()
        search_result = {
            'en':word,
            'cn':'',
            'uk_ph':'',
            'us_ph':'',
            'gen_ph':'',
        }
        try:
            page_src = ifind_parse.get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index",max_retry=1)
        except requests.exceptions.RequestException:
            search_result['cn']='网络异常'
            return search_result
        self.items = ifind_parse.parse_one_page(page_src)
        self.phonetics = ifind_parse.get_phonetic(page_src, print_status=False)
        self.last_search = word
        # print(self.phonetics)
        if self.items is not None and len(self.items):
            for i in self.items:
                search_result['cn'] += i
            self.pushButton_3.setEnabled(True)
        else:
            search_result['cn'] = '未找到词典信息'
            return search_result
        if len(self.phonetics['us']):
            # print(self.phonetics['us'][0])
            search_result['us_ph'] = (self.phonetics['us'][0])
        if len(self.phonetics['uk']):
            # print(self.phonetics['us'][0])
            search_result['uk_ph'] = (self.phonetics['uk'][0])
        if len(self.phonetics['common']):
            # print(self.phonetics['common'][0])
            search_result['gen_ph'] = self.phonetics['common'][0]
        return search_result

    def searchClicked(self):
        self.label_4.setText('查找...')
        result = self.search()
        self.setTable(result, type='search_result')
        self.label_4.setText('展示搜索结果.')

    def addClicked(self):
        self.label_4.setText('同步数据至数据库...')
        self.pushButton_3.setEnabled(False)
        str = ''
        for i in self.items:
            str += i
        if not len(self.wordlist.search_sqlite(self.last_search)):
            retmsg = self.wordlist.add_new_word(self.last_search,str)
        else:
            retmsg = '已录入，无需重复录入.'
        self.getWordlist()
        self.initTable()
        self.label_4.setText(retmsg)

    def getWordlist(self):
        self.wordlist = _wordlist.WordList(sqlite_dbname=os.path.join(sys.path[0], 'wordlist.db'))
        self.wordlist.sort_by_alphabet()

    def setTable(self,wordlist,type='wordlist'):
        t1 = time.time()
        self.table.horizontalHeader().setStretchLastSection(True)
        if type != 'search_result':
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(['英文', '中文'])
            rows = len(wordlist)
            self.table.setRowCount(rows)
        else:
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['英文', '中文', '英音标', '美音标', '通用音标'])
            rows = 1
            self.table.setRowCount(rows)
        rowcount = 0
        if type == 'wordlist':
            for i in wordlist:
                item0 = QtWidgets.QTableWidgetItem(i.it_self())
                item0.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(rowcount, 0, item0)
                item1 = QtWidgets.QTableWidgetItem(i.explanation())
                item1.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(rowcount, 1, item1)
                rowcount += 1
        elif type == 'query':
            for i in wordlist:
                item0 = QtWidgets.QTableWidgetItem(i[0])
                item0.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(rowcount, 0, item0)
                item1 = QtWidgets.QTableWidgetItem(i[1])
                item1.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(rowcount, 1, item1)
                rowcount += 1
        elif type == 'search_result':
            col_count = 0
            for i in wordlist:
                item = QtWidgets.QTableWidgetItem(wordlist[i])
                item.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(0, col_count, item)
                col_count += 1

        print('table set:',time.time()-t1)

    def initTable(self):
        self.setTable(self.wordlist,'wordlist')

    def refreshClicked(self):
        self.pushButton_3.setEnabled(False)
        self.initTable()
        self.pushButton_3.setEnabled(True)

    def filter(self):
        self.pushButton_3.setEnabled(False)
        query = self.wordlist.fuzzsearch_sqlite(self.lineEdit_2.text())
        query2 = sorted(query, key=lambda x: x[0])
        self.setTable(query2, type='query')
        self.label_4.setText('筛选完成.共'+str(len(query2))+'个结果')
        # if not len(query):
        #     self.pushButton_4.setEnabled(True)


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(318, 371)
        self.getWordlist()
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
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table = QtWidgets.QTableWidget(self.tab_2)
        self.table.setMaximumSize(QtCore.QSize(3000, 2000))
        self.table.setObjectName("table")
        self.initTable()
        self.gridLayout_2.addWidget(self.table, 3, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(3000, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setMaximumSize(QtCore.QSize(200, 30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
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
        self.pushButton_4.clicked.connect(self.searchClicked)
        self.pushButton_3.clicked.connect(self.addClicked)
        self.lineEdit_2.textChanged.connect(self.filter)
        self.pushButton_4.setEnabled(True)
        self.pushButton_3.setEnabled(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "iFindWord v1.3.1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "词库"))
        self.pushButton_3.setText(_translate("Dialog", "添加"))
        self.label_4.setText(_translate("Dialog", "就绪"))
        self.label.setText(_translate("Dialog", "软件地址：<a href=\"https://github.com/Hycdog/iFindWord/\">https://github.com/Hycdog/iFindWord</a>"))
        self.label.setOpenExternalLinks(True)
        self.label_2.setText(_translate("Dialog", "made by <a href=\"https://github.com/Hycdog/\">HycDog</a><p> Email: tubao9hao@126.com</p>"))
        self.label_2.setOpenExternalLinks(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "关于"))
        self.pushButton_4.setText(_translate("Dialog", "在线搜索"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
