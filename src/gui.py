# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first.ui'
#
# Created by: src UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets
import ifind_parse
import _wordlist
import time
import requests
import bitarray
class Ui_Dialog(object):

    def search(self):
        word = self.lineEdit.text()
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
            self.addWordButton.setEnabled(True)
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
        self.infoLabel_tab1.setText('查找...')
        result = self.search()
        self.setTable(result, type='search_result')
        self.infoLabel_tab1.setText('展示搜索结果.')

    def addClicked(self):
        self.infoLabel_tab1.setText('同步数据至数据库...')
        self.addWordButton.setEnabled(False)
        str = ''
        for i in self.items:
            str += i
        if not len(self.wordlist.search_sqlite(self.last_search)):
            retmsg = self.wordlist.add_new_word(self.last_search,str)
        else:
            retmsg = '已录入，无需重复录入.'
        self.getWordlist()
        self.initTable()
        self.infoLabel_tab1.setText(retmsg)

    def getWordlist(self):
        self.wordlist = _wordlist.WordList(sqlite_dbname=os.path.join(os.getcwd(), 'wordlist.db'))
        self.wordlist.sort_by_alphabet()

    def setTable(self,wordlist,type='wordlist'):
        t1 = time.time()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setHidden(True)
        self.laststate = bitarray.bitarray(len(wordlist))
        self.laststate.setall(False)
        if type != 'search_result':
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(['英文', '中文'])
            rows = len(wordlist)
            self.table.setRowCount(rows)
        else:
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['英文', '中文', '英音标', '美音标', '通用音标'])
            self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setStretchLastSection(False)

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
            self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            self.table.horizontalHeader().setStretchLastSection(False)
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
                # check = QtWidgets.QTableWidgetItem()
                # check.setCheckState(QtCore.Qt.Unchecked)
                # self.table.setItem(rowcount,1,check)

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
        self.addWordButton.setEnabled(False)
        self.initTable()
        self.addWordButton.setEnabled(True)

    def filter(self):
        self.addWordButton.setEnabled(False)
        query = self.wordlist.fuzzsearch_sqlite(self.lineEdit.text())
        query2 = sorted(query, key=lambda x: x[0])
        self.setTable(query2, type='query')
        self.infoLabel_tab1.setText('筛选完成.共'+str(len(query2))+'个结果')
        # if not len(query):
        #     self.searchOnlineButton.setEnabled(True)


    def showPos(self):
        length = self.table.rowCount()
        curstate = bitarray.bitarray(length)
        curstate.setall(False)
        for i in range(self.table.rowCount()):
            if self.table.item(i,1).checkState():
                curstate[i] = 1
        if bitarray.bitdiff(curstate, self.laststate):
            self.laststate = curstate
            # print(curstate)
            # insert funcion here



    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 320)
        self.getWordlist()
        # gridLayout that sets the tab to the center of the window
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        # General tab widget
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 281, 331))
        self.tabWidget.setObjectName("tabWidget")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(400, 400))
        self.tabWidget.setSizeIncrement(QtCore.QSize(1, 1))
        # First tab that contains searching result and table filled with data read from db.
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        # Grid layout for tab #1
        self.gridLayout_tab_1 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_tab_1.setObjectName("gridLayout_tab_1")
        # Top line that enables users to search
        # Along with search button that follows the lineEdit
        self.horizontalLayout_1_tab1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1_tab1.setObjectName("horizontalLayout_1_tab1")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(3000, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_1_tab1.addWidget(self.lineEdit)
        self.searchOnlineButton = QtWidgets.QPushButton(self.tab_1)
        self.searchOnlineButton.setMaximumSize(QtCore.QSize(200, 30))
        self.searchOnlineButton.setObjectName("searchOnlineButton")
        self.horizontalLayout_1_tab1.addWidget(self.searchOnlineButton)
        self.gridLayout_tab_1.addLayout(self.horizontalLayout_1_tab1, 2, 0, 1, 1)
        # Table that contains words and explanations directly read from sqlite db
        # Initialized in initTable()
        self.table = QtWidgets.QTableWidget(self.tab_1)
        self.table.setMaximumSize(QtCore.QSize(3000, 2000))
        self.table.setObjectName("table")
        self.initTable()
        self.gridLayout_tab_1.addWidget(self.table, 3, 0, 1, 1)
        # Button that adds word 
        self.addWordButton = QtWidgets.QPushButton(self.tab_1)
        self.addWordButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.addWordButton.setObjectName("addWordButton")
        self.gridLayout_tab_1.addWidget(self.addWordButton, 4, 0, 1, 1)
        # A Line that contains search button, isn't that satisfying.
        # Only temporary solution.
        self.horizontalLayout_2_tab1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2_tab1.setObjectName("horizontalLayout_2_tab1")
        self.addWordButton = QtWidgets.QPushButton(self.tab_1)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addWordButton.sizePolicy().hasHeightForWidth())
        self.addWordButton.setSizePolicy(sizePolicy)
        self.addWordButton.setMinimumSize(QtCore.QSize(88, 30))
        self.addWordButton.setMaximumSize(QtCore.QSize(88888, 30))
        self.addWordButton.setObjectName("addWordButton")
        self.horizontalLayout_2_tab1.addWidget(self.addWordButton)
        # self.checkBox = QtWidgets.QCheckBox(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        # self.checkBox.setSizePolicy(sizePolicy)
        # self.checkBox.setMaximumSize(QtCore.QSize(88888, 88888))
        # self.checkBox.setObjectName("checkBox")
        # self.horizontalLayout_2_tab1.addWidget(self.checkBox)
        self.gridLayout_tab_1.addLayout(self.horizontalLayout_2_tab1, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        # infoLabel is on the bottom of tab1, showing current status of the software.
        self.infoLabel_tab1 = QtWidgets.QLabel(self.tab_1)
        self.infoLabel_tab1.setObjectName("infoLabel_tab1")
        self.gridLayout_tab_1.addWidget(self.infoLabel_tab1, 5, 0, 1, 1)
        # tab_2  contains information about the contributors to this software,
        # as well as the github repo URL.
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_tab_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_tab_2.setObjectName("gridLayout_tab_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout_tab_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        # More comments needed
        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.searchOnlineButton.clicked.connect(self.searchClicked)
        self.addWordButton.clicked.connect(self.addClicked)
        self.lineEdit.textChanged.connect(self.filter)
        self.searchOnlineButton.setEnabled(True)
        self.addWordButton.setEnabled(False)
        # self.table.clicked.connect(self.showPos)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "iFindWord v1.3.6"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Dialog", "词库"))
        self.addWordButton.setText(_translate("Dialog", "添加"))
        self.infoLabel_tab1.setText(_translate("Dialog", "就绪"))
        # self.checkBox.setText(_translate("Dialog", "监控剪贴板"))
        self.label.setText(_translate("Dialog", "软件地址：<a href=\"https://github.com/Hycdog/iFindWord/\">https://github.com/Hycdog/iFindWord</a>"))
        self.label.setOpenExternalLinks(True)
        self.label_2.setText(_translate("Dialog", "made by <a href=\"https://github.com/Hycdog/\">HycDog</a><p> Email: tubao9hao@126.com</p>"))
        self.label_2.setOpenExternalLinks(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "关于"))
        self.searchOnlineButton.setText(_translate("Dialog", "在线搜索"))



if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
