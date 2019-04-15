import ctypes
import re
import pandas
import smtplib
import random
import os
import getpass
import sys
import getopt
import subprocess
import contextlib
import decimal
import zipfile
import datetime
import copy
import time
import pyperclip
try:
    import matplotlib.pyplot as plt
except:
    pass
import selenium
import requests
import pymysql
from random import choice
from requests.exceptions import RequestException
from datetime import date
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contextlib import closing
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from decimal import Decimal
from requests.exceptions import ConnectionError

def get_path():
    path_file = __file__
    folder_path = re.search("(.*)/", path_file)
    if folder_path is None:#
        folder_path = re.search(r"(.*)\\", path_file)#为什么要这么写呢，因为ctmd在cmd里的路径是用的反斜杠，在ide里用的是正斜杠
    try:
        return folder_path.group()
    except:
        return ""


class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0,
                 ):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.sep = sep
        self.percentage = count/total*100
        self.percentmark = '%'

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count / self.chunk_size, self.unit, self.sep, self.total / self.chunk_size, self.unit, self.percentage, self.percentmark)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status != None:
        self.percentage = self.count/self.total*100
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

date_today = str(date.today())
chromedriver_lookup = {
    "29": "2.4",
    "30": "2.7",
    "31": "2.9",
    "32": "2.9",
    "33": "2.10",
    "34": "2.10",
    "35": "2.10",
    "36": "2.12",
    "37": "2.12",
    "38": "2.13",
    "39": "2.14",
    "40": "2.15",
    "41": "2.15",
    "42": "2.17",
    "43": "2.20",
    "44": "2.20",
    "45": "2.20",
    "46": "2.21",
    "47": "2.21",
    "48": "2.21",
    "49": "2.22",
    "50": "2.22",
    "51": "2.23",
    "52": "2.24",
    "53": "2.26",
    "54": "2.27",
    "55": "2.28",
    "56": "2.29",
    "57": "2.29",
    "58": "2.31",
    "59": "2.32",
    "60": "2.33",
    "61": "2.34",
    "62": "2.35",
    "63": "2.36",
    "64": "2.37",
    "65": "2.38",
    "66": "2.40",
    "67": "2.41",
    "68": "2.42",
    "69": "2.42",
    "70": "2.42",
    "71": "70.0.3538.16",
}
minimum_requirement = 29
maximum_support = 71
known_issue = [
    "无",
]
to_do = [
]

class Atom:
    def __init__(self, date=str(date.today()), testedcount=0, searchcount=0, inputcount=0):
        self.__date = date
        self.__testedCount = testedcount
        self.__searchCount = searchcount
        self.__inputCount = inputcount

    def tested_count(self):
        return self.__testedCount

    def searched_count(self):
        return self.__searchCount

    def input_count(self):
        return self.__inputCount

    def get_date(self):
        return self.__date

    def tested(self):
        self.__testedCount += 1

    def searched(self):
        self.__searchCount += 1

    def grow(self):
        self.__inputCount += 1

    def numeric_data(self):
        return str(self.__testedCount)+" "+str(self.__searchCount)+" "+str(self.__inputCount)

    def show_info(self):
        print(self.__date, "录入了", self.__inputCount, "个单词, 搜索了",self.__searchCount,"次, 做了",self.__testedCount,"题")


class Fusion:

    __Reactor = []

    def read_date_from_file(self, filename=None):
        if filename is None:
            filename = self.__filename
        try:
            f = open(filename, "r", encoding="utf-8-sig")
            strn = f.read()
            fpt = {}
            res = re.split('\n', strn)
            for i in range(1, len(res), 2):
                fpt[res[i - 1].replace("\s", "")] = []
                numeric_data = res[i].split(' ')
                for j in numeric_data:
                    fpt[res[i - 1].replace("\s", "")].append(int(j))
            f.close()
        except FileNotFoundError:
            f = open(filename, "w+", encoding="utf-8")
            fpt = {}
            f.close()
        except UnicodeDecodeError:
            f = open(filename, "r", encoding="utf-8")
            strn = f.read()
            fpt = {}
            res = re.split('\n', strn)
            for i in range(1, len(res), 2):
                fpt[res[i - 1].replace("\s", "")] = []
                numeric_data = res[i].split(' ')
                for j in numeric_data:
                    fpt[res[i - 1].replace("\s", "")].append(int(j))
        for i in fpt:
            a_single_atom = Atom(i, int(fpt[i][0]), int(fpt[i][1]), int(fpt[i][2]))
            self.__Reactor.append(a_single_atom)
        if self.today() is None:
            self.add_atom(date_today)

    def write_date_to_file(self, filename=None):
        if filename is None:
            filename = self.__filename
        f = open(filename, "w+", encoding="utf-8")
        for i in self.__Reactor:
            f.write(i.get_date() + "\n")
            f.write(i.numeric_data() + '\n')
        f.close()

    def __init__(self, filename=None):
        if filename is not None:
            self.__Reactor = []
            self.__filename = filename
            self.read_date_from_file(filename)
        else:
            self.__Reactor = []

    def __len__(self):
        return len(self.__Reactor)

    def __iter__(self):
        return iter(self.__Reactor)

    def today(self):
        for atom in self.__Reactor:
            if atom.get_date() == str(date.today()):
                return atom
        return None

    def tested_most(self, show=False):
        if len(self.__Reactor) is not 0:
            self.__Reactor = sorted(self.__Reactor, key=lambda atom: atom.tested_count(), reverse=True)
            theatom = self.__Reactor[0]
            if show:
                print(theatom.get_date(), " 做题最多, 做了", theatom.tested_count(), "题")
            self.__Reactor = sorted(self.__Reactor, key=lambda atom: atom.get_date(), reverse=False)
            return theatom
        else:
            return None

    def searched_most(self, show=False):
        if len(self.__Reactor) is not 0:
            self.__Reactor = sorted(self.__Reactor, key=lambda atom: atom.searched_count(), reverse=True)
            theatom = self.__Reactor[0]
            if show:
                print(theatom.get_date(), " 搜词最多, 搜了", theatom.searched_count(), "题")
            self.__Reactor = sorted(self.__Reactor, key=lambda atom: atom.get_date(), reverse=False)
            return theatom
        else:
            return None

    def input_most(self, show=False):
        if len(self.__Reactor) is not 0:
            self.__Reactor = sorted(self.__Reactor, key=lambda atom: atom.input_count(), reverse=True)
            theatom = self.__Reactor[0]
            if show:
                print(theatom.get_date(), " 录入最多, 录了", theatom.input_count(), "题")
            self.__Reactor = sorted(self.__Reactor, key=lambda atom: atom.get_date(), reverse=False)
            return theatom
        else:
            return None

    def add_atom(self, datestr):
        new_atom = Atom(datestr)
        self.__Reactor.append(new_atom)


class Word:

    def __init__(self, enword, cnexplanation, testedcount=0, correctcount=0, searchtime=0, recordedtime=str(datetime.datetime.now())):
        self.__enWord = enword
        self.__cnExplanation = cnexplanation
        self.__testedCount = testedcount
        self.__correctCount = correctcount
        self.__searchTime = searchtime
        self.__Visited = False
        self.__recordedTime = recordedtime
        self.__recordedDate = recordedtime[0:10]

    def it_self(self, mysql_format=False):
        if not mysql_format:
            return self.__enWord
        else:
            return str(repr(self.__enWord))

    def explanation(self, mysql_format=False):
        if not mysql_format:
            return self.__cnExplanation
        else:
            return str(repr(self.__cnExplanation))

    def tested_count(self, mysql_format=False):
        if not mysql_format:
            return self.__testedCount
        else:
            return str(repr(str(self.__testedCount)))

    def correct_count(self, mysql_format=False):
        if not mysql_format:
            return self.__correctCount
        else:
            return str(repr(str(self.__correctCount)))

    def recorded_date(self, mysql_format=False):
        if not mysql_format:
            return self.__recordedDate
        else:
            return str(repr(self.__recordedDate))

    def recorded_time(self, mysql_format=False):
        if not mysql_format:
            return self.__recordedTime
        else:
            return str(repr(self.__recordedTime))

    def incorrect_count(self, mysql_format=False):
        if not mysql_format:
            return self.__testedCount-self.__correctCount
        else:
            return str(repr(str(self.__testedCount-self.__correctCount)))

    def searched_count(self, mysql_format=False):
        if not mysql_format:
            return self.__searchTime
        else:
            return str(repr(str(self.__searchTime)))

    def visited(self, mysql_format=False):
        if not mysql_format:
            return self.__Visited
        else:
            return str(repr(int(self.__Visited)))

    def correct_rate(self):
        return round(Decimal(self.__correctCount/self.__testedCount * 100.0), 2)

    def incorrect_rate(self):
        return round(Decimal((self.__testedCount-self.__correctCount) / self.__testedCount* 100.0), 2)

    def numeric_data(self):
        return str(self.__testedCount)+" "+str(self.__correctCount)+" "+str(self.__searchTime)

    def correct(self):
        self.__testedCount += 1
        self.__correctCount += 1

    def incorrect(self):
        self.__testedCount += 1

    def searched(self):
        self.__searchTime += 1

    def show_rate(self):
        print(self.it_self(), "已做", self.tested_count(), "次，正确", self.correct_count(), "次，正确率", self.correct_rate(), "%")#在1.8.2版本修复

    def visit(self):
        self.__Visited = True

    def unvisit(self):
        self.__Visited = False

    def change_explanation(self, new_explanation):
        self.__cnExplanation = new_explanation

    def is_phrase(self):
        k = self.__enWord.split(' ')
        return len(k)>1


class WordList:
    __wordList = []
    __engList = []
    __unvisitedList = []
    __phraseList = []
    __recentList = []

    def init_visit_status(self):
        self.__unvisitedList = []
        for word in self.__wordList:
            if not word.visited():
                self.__unvisitedList.append(word)

    def save_to_mysqldb(self, db_name="dj", table_name = "wordlist"):
        host = input("host:")
        username = input("username:")
        password = getpass.getpass("password:")  # console usage
        # password = input("password:") # ide usage
        db = pymysql.connect(host, username, password)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS "+db_name)
        cursor.execute("USE " + db_name)
        cursor.execute("DROP TABLE IF EXISTS WORDLIST")
        sql = """CREATE TABLE WORDLIST (
                 ENGLISH  VARCHAR(100) NOT NULL,
                 CHINESE  VARCHAR(300) NOT NULL,
                 TESTED_COUNT INT,
                 CORRECT_COUNT INT,
                 SEARCHED_TIMES INT,
                 RECORDED_TIME CHAR(30) NOT NULL,
                 VISITED BOOLEAN)"""
        cursor.execute(sql)
        finished_count = 0
        total_count = len(self.__wordList)
        migrate_progress = ProgressBar("同步数据至数据库...", total=total_count, unit="", chunk_size=1, run_status="正在同步",
                                      fin_status="同步完成")
        for word in self.__wordList:
            sql_insert = """INSERT INTO """+table_name+"""(ENGLISH,
                 CHINESE, TESTED_COUNT, CORRECT_COUNT, SEARCHED_TIMES, RECORDED_TIME, VISITED)
                 VALUES (""" + word.it_self(mysql_format=True) + "," + word.explanation(mysql_format=True) + "," + \
                         word.tested_count(mysql_format=True) + "," + word.correct_count(mysql_format=True) + "," + \
                         word.searched_count(mysql_format=True) + "," + word.recorded_time(mysql_format=True) + "," + \
                         word.visited(mysql_format=True) + ")"
            try:
                cursor.execute(sql_insert)
                # 提交到数据库执行
                db.commit()
                finished_count += 1
                migrate_progress.refresh(count=1)
            except:
                # 如果发生错误则回滚
                db.rollback()
                print("执行第", finished_count+1, "个时发生错误。数据库已回滚")
                print(word)
        # 关闭数据库连接
        print(finished_count, "/", total_count, "完成")
        db.close()

    def read_wordlist_from_file(self, filename=None):
        if filename is None:
            filename = self.__filename
        try:
            fpt = {}
            f = open(filename, "r", encoding="utf-8-sig")  # qnmd \ufeff 我真的佛了
            pre_f = f.read()
            post_f = re.split('\n', pre_f)
            for i in range(1, len(post_f), 4):
                fpt[post_f[i - 1].replace("\s", "")] = [post_f[i].replace("\s", "")]
                numeric_data = post_f[i + 1].split(' ')
                for j in numeric_data:
                    fpt[post_f[i - 1].replace("\s", "")].append(j)
                fpt[post_f[i - 1].replace("\s", "")].append(post_f[i+2].strip())
            f.close()
        except FileNotFoundError:
            f = open(filename, "w+", encoding="utf-8")
            fpt = {}
            f.close()
        except UnicodeDecodeError:
            fpt = {}
            f = open(filename, "r")
            pre_f = f.read()
            post_f = re.split('\n', pre_f)
            for i in range(1, len(post_f), 3):
                fpt[post_f[i - 1]] = [post_f[i]]
                numeric_data = post_f[i + 1].split(' ')
                for j in numeric_data:
                    fpt[post_f[i - 1]].append(j)
            f.close()
        for i in fpt:
            singleword = Word(i, fpt[i][0], int(fpt[i][1]), int(fpt[i][2]), int(fpt[i][3]), str(fpt[i][4]))
            self.__wordList.append(singleword)
            self.__engList.append(singleword.it_self())
            if singleword.is_phrase():
                self.__phraseList.append(singleword)

    def write_wordlist_to_file(self, filename=None):
        if filename is None:
            filename = self.__filename
        f = open(filename, "w+", encoding="utf-8")
        self.sort_by_alphabet() # v1.7.6 加入
        for i in self.__wordList:
            f.write(i.it_self() + "\n")
            f.write(i.explanation() + "\n")
            f.write(i.numeric_data() + "\n")
            f.write(str(i.recorded_time())+'\n')
        f.close()

    def __init__(self, source="file", filename=None, mysql_dbname = None):
            if source == "file":
                if filename is not None:
                    self.__wordList = []
                    self.__engList = []
                    self.__unvisitedList = []
                    self.__phraseList = []
                    self.__filename = filename
                    self.read_wordlist_from_file(filename)
                    self.init_visit_status()
                    self.sort_by_alphabet()
                else:
                    self.__wordList = []
                    self.__engList = []
                    self.__unvisitedList = []
                    self.__phraseList = []


    def __iter__(self):
        return iter(self.__wordList)

    def __len__(self):
        return len(self.__wordList)

    def delete_word(self, wordname):
        self.__engList.remove(wordname.it_self())
        self.__wordList.remove(wordname)
        if wordname in self.__unvisitedList:
            self.__unvisitedList.remove(wordname)
        if wordname in self.__phraseList:
            self.__phraseList.remove(wordname)

    def eng_list(self):
        return self.__engList

    def complete_list(self):
        return self.__wordList

    def get_unvisited_list(self, sort_by_time = False, sort_reverse = False):
        if sort_by_time:
            self.__unvisitedList = sorted(self.__unvisitedList, key=lambda x: x.recorded_time(), reverse=sort_reverse)
        return self.__unvisitedList

    def phrase_count(self):
        return len(self.__phraseList)

    def phrase_list(self):
        return self.__phraseList

    def search(self, en_word):
        for word in self.__wordList:
            if word.it_self() == en_word:
                return word
        return None

    def add_new_word(self, en_word, cn_word):
        newWord = Word(en_word, cn_word, recordedtime=str(datetime.datetime.now()))
        self.__wordList.append(newWord)
        self.__unvisitedList.append(newWord)
        self.__engList.append(newWord.it_self())
        if newWord.is_phrase():
            self.__phraseList.append(newWord)
        print(newWord.it_self(), newWord.explanation())
        print("录入时间：", newWord.recorded_time())

    def add_Word(self, newWord):
        self.__wordList.append(newWord)
        self.__unvisitedList.append(newWord)
        self.__engList.append(newWord.it_self())
        if newWord.is_phrase():
            self.__phraseList.append(newWord)

    def visit(self, word):
        self.__unvisitedList.remove(word)
        word.visit()

    def sort_by_rate(self):
        self.__wordList = sorted(self.__wordList, key=lambda x: x.incorrect_rate())
        return self.__wordList

    def sort_by_alphabet(self):
        self.__wordList = sorted(self.__wordList, key=lambda x: x.it_self())
        return self.__wordList

    def sort_by_date(self):
        self.__wordList = sorted(self.__wordList, key=lambda x: x.recorded_date())
        return self.__wordList

    def sort_by_time(self, reverse=False):
        self.__wordList = sorted(self.__wordList, key=lambda x: x.recorded_time(), reverse=reverse)
        return self.__wordList

    def get_list_today(self):
        __wordListToday = []
        for word in self.__wordList:
            if word.recorded_date() == date_today:
                __wordListToday.append(word)
        return __wordListToday

    def show_everything(self):
        # def __init__(self, enword, cnexplanation, testedcount=0, correctcount=0, searchtime=0, recordedtime=str(datetime.datetime.now())):
        for word in self.__wordList:
            print(word.it_self(), word.explanation())
            print("录入时间：", word.recorded_time())
            print("做了:", word.tested_count(), "次", "对了:", word.correct_count(), "次", "搜过", word.searched_count(),"次")


def save_to_orclpdb(wordlist):
    pass

def show_menu():
    print("1:显示所有单词和词组")
    print("3:按时间顺序测试")
    print("4:随机测试hint always版")
    print("5:本地模糊查找单词")
    print("6:按时间顺序显示")
    print("7:错题集")
    print("8:自动录入chrome版")
    print("9:随机测试英译中")
    print("0:其他功能")


def show_sub_menu():
    print("2:统计数据")
    print("3:把所有单词及词组替换成有道词典版本")
    print("6:显示所有词组")
    print("7:显示今日录入")
    print("8:所有单词按录入日期排序")
    print("9:显示所有单词所有信息")
    print("0:返回主菜单")


def on_progress():
    print("该功能还在开发中！")


def test_done(p, datelist, wordlist, correct=False ,savefile = True):
    if correct:
        p.correct()
    else:
        p.incorrect()
    datelist.today().tested()
    datelist.write_date_to_file()
    p.show_rate()
    if savefile:
        wordlist.write_wordlist_to_file()


def statistics(wordlist, datelist):
    for i in datelist:
        i.show_info()
    print("共有", len(wordlist), "个单词及词组收录。")
    datelist.searched_most(show=True)
    datelist.input_most(show=True)
    datelist.tested_most(show=True)
    print("\n今天：")
    datelist.today().show_info()


def print_graph(datelist):
    names = []
    values_search = []
    values_input = []
    values_test = []
    for i in datelist:
        names.append(i.get_date())
        values_search.append(i.searched_count())
        values_input.append(i.input_count())
        values_test.append(i.tested_count())
    plt.plot(names, values_input, '-', label="Input Count")
    plt.plot(names, values_search, '-', label="Search Count")
    plt.plot(names, values_test, '-', label="Test Count")
    plt.legend()
    plt.suptitle('in development...')
    plt.show()


def mistake_collection(wordlist, datelist):
    soup = WordList()
    for i in wordlist:
        if i.incorrect_count() > 0:
            soup.add_Word(i)
    soup.sort_by_rate()
    for i in soup:
        i.show_rate()
    print("准备好进行错题测试吗？（y/n)")
    chx = input().strip().lower()
    while len(chx) == 0:
        chx = input().strip().lower()
    if chx == 'y':
        random_test_hint_always(soup, datelist, savefile=False)
    return soup


def random_test_hint_always(wordlist, datelist, recent=False, savefile=True):
    if not recent:
        p = choice(wordlist.get_unvisited_list())
    else:
        p = wordlist.get_unvisited_list(True, True)[0]
    wordlist.visit(p)
    p2 = p
    p3 = p
    print(p.explanation()),
    print("对应哪个单词？(输入Ctrl+C退出)")
    if len(wordlist.get_unvisited_list()) > 0:
        p2 = choice(wordlist.get_unvisited_list())
    if len(wordlist.get_unvisited_list()) > 1:
        p3 = choice(wordlist.get_unvisited_list())
        while p3 == p2:
            p3 = choice(wordlist.get_unvisited_list())
    seed = random.randint(0, 2)
    if seed == 0:
        if len(wordlist.get_unvisited_list()) == 0:
            genuine_pos = 0
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            print("提供以下两个选择:"), print(p.it_self(), ",", p2.it_self())
            genuine_pos = 0
        else:
            print("提供以下三个选择:"), print(p.it_self(), ",", p2.it_self(), ",", p3.it_self())
            genuine_pos = 0
    elif seed == 1:
        if len(wordlist.get_unvisited_list()) == 0:
            genuine_pos = 0
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            genuine_pos = 1
            print("提供以下两个选择:"), print(p2.it_self(), ",", p.it_self())
        else:
            genuine_pos = 1
            print("提供以下三个选择:"), print(p2.it_self(), ",", p.it_self(), ",", p3.it_self())
    elif seed == 2:
        if len(wordlist.get_unvisited_list()) == 0:
            genuine_pos = 0
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            genuine_pos = 0
            print("提供以下两个选择:"), print(p.it_self(), ",", p2.it_self())
        else:
            genuine_pos = 2
            print("提供以下三个选择:"), print(p2.it_self(), ",", p3.it_self(), ",", p.it_self())
    ans = input().strip().lower()
    while len(ans) == 0:
        ans = input().strip().lower()
    if ans == "exit()":
        return False
    if ans == p.it_self() or ans == str(genuine_pos+1):
        if len(wordlist.get_unvisited_list()) == 0:
            print("你已经全部都答完啦！")
            try:
                page_src = get_one_page("http://dict.youdao.com/w/" + p.it_self() + "/#keyfrom=dict2.index")
                get_phonetic(page_src)
            except:
                pass
            test_done(p, datelist, wordlist, True, savefile)
            return
        else:
            try:
                page_src = get_one_page("http://dict.youdao.com/w/" + p.it_self() + "/#keyfrom=dict2.index")
                get_phonetic(page_src)
            except:
                pass
            test_done(p, datelist, wordlist, True, savefile)
            random_test_hint_always(wordlist, datelist, recent, savefile)
    else:
        print("正确答案是:", p.it_self())
        try:
            page_src = get_one_page("http://dict.youdao.com/w/" + p.it_self() + "/#keyfrom=dict2.index")
            get_phonetic(page_src)
        except:
            pass
        test_done(p, datelist, wordlist, False)
        random_test_hint_always(wordlist, datelist, recent, savefile)


def new_word_auto_chrome(wordlist, datelist):
    try:
        word_cn = ""
        word_cn_complete_youdao = ""
        word_cn_complete_baidu = ""
        word_cn_complete_baidufanyi = ""
        print("输入英文:(输入 Ctrl+C 取消录入)")
        word = input().strip().lower()
        while len(word) == 0:
            word = input().strip().lower()
        result = wordlist.search(word)
        while result is not None:
            print(result.it_self(), result.explanation())
            datelist.today().searched()
            print(word, "已经存在，请重新输入")
            word = input().strip().lower()
            while len(word) == 0:
                word = input().strip().lower()
            if word == "exit()":
                print("已取消录入")
                return False
            result = wordlist.search(word)
        try:
            browser0 = webdriver.Chrome()
        except WebDriverException:
            print("Chrome无法正常打开，可能是未安装chromedriver，是否下载安装？(y/n)")
            chk = input().strip().lower()
            while len(chk) == 0:
                chk = input().strip().lower()
            if chk == 'y':
                print('请打开chrome浏览器，右上角，下拉菜单选择"帮助"，"关于Google Chrome"，复制版本数字并粘贴在此处')
                chromemirror_url = r"http://npm.taobao.org/mirrors/chromedriver/"
                chromedriver_name = r"/chromedriver_win32.zip"
                while True:
                    ver_str = input().strip()
                    if len(ver_str) < 2:
                        print("请输入正确的版本号！")
                    else:
                        try:
                            ver_num = int(ver_str[0:2])
                            break
                        except ValueError:
                            print("请输入正确的版本号！")
                try:
                    download_url = chromemirror_url + chromedriver_lookup[
                        ver_str] + chromedriver_name  # 记住字典里的key是字符串！所以不能用ver_num
                    with closing(requests.get(download_url, stream=True)) as response:
                        chunk_size = 1024
                        content_size = int(response.headers['content-length'])
                        """
                        需要根据 response.status_code 的不同添加不同的异常处理
                        """
                        # print('content_size', content_size, response.status_code, )
                        progress = ProgressBar("chromedriver v"+chromedriver_lookup[ver_str]
                                               , total=content_size
                                               , unit="KB"
                                               , chunk_size=chunk_size
                                               , run_status="正在下载"
                                               , fin_status="下载完成")
                        # chunk_size = chunk_size < content_size and chunk_size or content_size
                        with open('chromedriver.zip', "wb") as file:
                            for data in response.iter_content(chunk_size=chunk_size):
                                file.write(data)
                                progress.refresh(count=len(data))
                        print('下载完成!')
                        z = zipfile.ZipFile('chromedriver.zip', 'r')
                        print("解压中...")
                        z.extractall(path=get_path())
                        z.close()
                        print("安装完成！")
                        
                        sys.exit()
                except ConnectionError:
                    print("下载失败，无法连接到服务器")
                    return False
                except KeyError:
                    if int(ver_num) < minimum_requirement:
                        print("很抱歉，您的chrome版本低于", minimum_requirement, "，无法使用该功能")
                        return False
                    elif int(ver_num) > maximum_support:
                        print("很抱歉，您的chrome版本高于", maximum_support, "，无法使用该功能")
                        return False
            else:
                return False
        wait = WebDriverWait(browser0, 5)
        browser0.get("https://www.baidu.com/")
        browser0.find_element_by_id("kw").send_keys(word)
        browser0.find_element_by_id("su").click()
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pc')))
            word_result = browser0.find_elements_by_class_name("op_dict3_english_result_table")
            if len(word_result) != 0:
                for i in word_result:
                    word_cn += i.text
                word_cn_complete_baidu = word_cn.replace('\n', "").replace('\r', "")
            raise TimeoutException
        except TimeoutException:
            browser0.get("https://fanyi.baidu.com/?aldtype=85#en/zh/" + word)
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dictionary-comment')))
                word_result = browser0.find_elements_by_class_name('dictionary-comment')
                for i in word_result:
                    word_cn += i.text
                word_cn_complete_baidufanyi = word_cn.replace('\n', "").replace('\r', "")
                raise TimeoutException
            except TimeoutException:
                browser0.get("http://dict.youdao.com/w/eng/" + word + "/#keyfrom=dict2.index")
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'trans-container')))
                    word_result = browser0.find_elements_by_css_selector('#phrsListTab > div.trans-container > ul > li')
                    for i in word_result:
                        word_cn += i.text
                    word_cn_complete_youdao = word_cn.replace('\n', "").replace('\r', "")
                    print(word_cn_complete_youdao)
                except TimeoutException:
                    pass
        found_at_least_one = False
        if len(word_cn_complete_baidu) != 0:
            print("1、百度搜索：", word_cn_complete_baidu)
            found_at_least_one = True
        else:
            print("百度搜索未找到匹配结果。")
        if len(word_cn_complete_baidufanyi) != 0:
            print("2、百度翻译：", word_cn_complete_baidufanyi)
            found_at_least_one = True
        else:
            print("百度翻译未找到匹配结果。")
        if len(word_cn_complete_youdao) != 0:
            print("3、有道词典：", word_cn_complete_youdao)
            found_at_least_one = True
        else:
            print("有道词典未找到匹配结果。")
        if found_at_least_one:
            datelist.today().searched()
            print("选择要录入的结果序号：(输入0退出)")
            cfm = input().strip().lower()
            while len(cfm) == 0:
                cfm = input().strip().lower()
            if cfm == "1":
                if len(word_cn_complete_baidu) != 0:
                    wordlist.add_new_word(word, word_cn_complete_baidu)
                    datelist.today().grow()
                    return True
                else :
                    print("已取消录入")
                    return False
            elif cfm == "2":
                if len(word_cn_complete_baidufanyi) != 0:
                    wordlist.add_new_word(word, word_cn_complete_baidufanyi)
                    datelist.today().grow()
                    return True
                else :
                    print("已取消录入")
                    return False
            elif cfm == "3":
                if len(word_cn_complete_youdao) != 0:
                    wordlist.add_new_word(word, word_cn_complete_youdao)
                    datelist.today().grow()
                    return True
                else:
                    print("已取消录入")
                    return False
            else:
                print("已取消录入")
                return False
        else:
            return False
    except NoSuchWindowException:
        print("窗口异常关闭，无法继续操作。")
        os.system("pause")
        return False
    except NoSuchElementException:
        print("网页无法正常加载。请检查网络连接？")
        os.system("pause")
        return False
    except WebDriverException:
        print("引擎异常，无法继续操作。")
        os.system("pause")
        return False


def parse_one_page(document):
    pattern = re.compile('''<div class="trans-container">\s*?<ul>\s*(.*?)\s*?</ul>''', re.S)
    items1 = re.search(pattern, document)
    pattern2 = re.compile("<li>(.*?)</li>", re.S)
    items = re.findall(pattern2, items1.group())
    return items


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        session = requests.session()
        response = session.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return
    except RequestException:
        raise RequestException


def new_word_auto_requests(wordlist, datelist):
    print("输入英文:(输入 Ctrl+C 取消录入)")
    word = input().strip().lower()
    while len(word) == 0:
        word = input().strip().lower()
    result = wordlist.search(word)
    while result is not None:
        print(result.it_self(), result.explanation())
        print(word, "已经存在，请重新输入")
        datelist.today().searched()
        word = input().strip().lower()
        while len(word) == 0:
            word = input().strip().lower()
        if word == "exit()":
            print("已取消录入")
            return False
        result = wordlist.search(word)
    try:
        page_src = get_one_page("http://dict.youdao.com/w/eng/"+word+"/#keyfrom=dict2.index")
    except RequestException:
        print("连接服务器异常。请检查网络连接？")
        os.system("pause")
        return False
    try:
        word_cn = ""
        items = parse_one_page(page_src)
        for i in items:
            word_cn += i
        word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
        word_cnt = word.split(' ')
        if len(word_cnt) is 1:
            print(word, word_cn_complete, "确认把这个单词加入列表吗?(Y/N)")
        else:
            print(word, word_cn_complete, "确认把这个词组加入列表吗?(Y/N)")
        datelist.today().searched()
        cfm = input().strip().lower()
        while len(cfm) == 0:
            cfm = input().strip().lower()
        if cfm == "Y" or cfm == "y":
            wordlist.add_new_word(word, word_cn_complete)
            datelist.today().grow()
            return True
        else:
            print("已取消录入")
            return False
    except AttributeError:
        print("有道词典未找到", word, "！")


def impatient_search(word, wordlist, datelist):
    word = word.strip().lower()#in version v 1.7.4
    result = wordlist.search(word)
    if result is not None:
        print(word, result.explanation(), " 已经录入本地词库")
        datelist.today().searched()
        result.searched()
        wordlist.write_wordlist_to_file()
        datelist.write_date_to_file()
        return False
    else:
        try:
            page_src = get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index")
        except RequestException:
            print("连接服务器异常...")
            return False
        try:
            word_cn = ""
            items = parse_one_page(page_src)
            for i in items:
                word_cn += i
            word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
            word_cnt = word.split(' ')
            if len(word_cnt) is 1:
                print(word, word_cn_complete, "要把这个单词加入列表吗?(Y/N)")
            else:
                print(word, word_cn_complete, "要把这个词组加入列表吗?(Y/N)")
            datelist.today().searched()
            cfm = input().strip().lower()
            while len(cfm) == 0:
                cfm = input().strip().lower()
            if cfm == "Y" or cfm == "y":
                wordlist.add_new_word(word, word_cn_complete)
                datelist.today().grow()
                wordlist.write_wordlist_to_file()
                datelist.write_date_to_file()
                return True
            else:
                datelist.write_date_to_file()
                return False
        except AttributeError:
            print("有道词典未找到", word, "！")


def replace_youdao(wordlist):
    print("即将替换", len(wordlist), "个单词/词组,如果没有在有道找到相关解释会跳过。是否继续？(y/n)")
    count = 0
    cfm = input().strip().lower()
    while len(cfm) == 0:
        cfm = input().strip().lower()
    if cfm == "Y" or cfm == "y":
        for word in wordlist:
            word_cn = ""
            try:
                page_src = get_one_page("http://dict.youdao.com/w/eng/" + word.it_self() + "/#keyfrom=dict2.index")
            except RequestException:
                print("连接服务器异常。请检查网络连接？")
                os.system("pause")
                return False
            try:
                items = parse_one_page(page_src)
                for i in items:
                    word_cn += i
                word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
                word.change_explanation(word_cn_complete)
                count += 1
                print(word.it_self(), word.explanation(), "替换成功", count, "/", len(wordlist))
            except AttributeError:
                count += 1
                print("有道词典未找到", word.it_self(), "！")
                continue
        wordlist.write_wordlist_to_file()
    else:
        print("已取消操作")
        return False


def fuzzy_finder(wordlist, datelist):
    suggestions = []
    print("输入您想查找的单词：")
    user_input = input().strip().lower()
    while len(user_input) == 0:
        user_input = input().strip().lower()
    result = wordlist.search(user_input)
    if result is not None:
        print(result.it_self(), result.explanation())
        datelist.today().searched()
        result.searched()
        wordlist.write_wordlist_to_file()
        return
    else:
        pattern = '.*'.join(user_input)  # Converts 'djm' to 'd.*j.*m'
        while True:
            regex = re.compile(pattern)  # Compiles wordlist regex.
            for item in wordlist:
                match = regex.search(item.it_self())  # Checks if the current item matches the regex.
                if match:
                    suggestions.append(item)
            if len(suggestions) != 0:
                print("您是否要找：")
                for i in suggestions:
                    print(i.it_self(), i.explanation())
                datelist.today().searched()
                return suggestions
            else:
                if len(pattern) > 3:
                    pattern = pattern[0:-2]
                else:
                    print("未找到任何结果！")
                    return


def show_word(wordlist, show_date_delimeter=False, show_by_time=False):
    if not show_date_delimeter:
        for i in wordlist:
            print(i.it_self(), i.explanation())
    elif not show_by_time:
        date_str = ""
        for i in wordlist:
            if date_str != i.recorded_date():
                date_str = i.recorded_date()
                print(date_str)
            print(i.it_self(), i.explanation())
    elif show_by_time:
        wordlist.sort_by_time()
        for i in wordlist:
            print(i.it_self(), i.explanation())


def show_phrases(wordlist):
    count = 0
    for i in wordlist:
        if i.is_phrase():
            print(i.it_self(),i.explanation())
            count += 1
    print("共", count, "个词组")


def monitor_clipboard(last_data, wordlist, datelist):
    while True:
        try:
            time.sleep(0.2)
            clip_data = pyperclip.paste()
            #
            if clip_data != last_data:
                pattern = re.compile("([^a-zA-Z0-9 \'\-]+)", re.S)
                filtered_word = re.findall(pattern, clip_data)
                if len(filtered_word) is 0 and len(clip_data) > 1:
                    impatient_search(clip_data, wordlist, datelist)
                else:
                    print("跳过无效信息")
                    # print(filtered_word)
                last_data = clip_data
                continue
        except TypeError:
            continue
        except KeyboardInterrupt:
            exit()


def get_phonetic(document):
    pattern_US = re.compile('''美\s*?<span class="phonetic">(.*?)</span>''', re.S)
    pattern_UK = re.compile('''英\s*?<span class="phonetic">(.*?)</span>''', re.S)
    pattern_common = re.compile('''\s*?<span class="phonetic">(.*?)</span>''', re.S)
    item_US = re.findall(pattern_US, document)
    item_UK = re.findall(pattern_UK, document)
    item_common = re.findall(pattern_common, document)
    items = {}
    items['us'] = item_US
    items['uk'] = item_UK
    items['common'] = item_common
    if len(items['uk']) == 0 and len(items['us']) == 0:
        if(len(item_common) == 0):
            print('未找到读音信息')
        else:
            print('音标:', items['common'][0])
    else:
        if len(items['uk']) != 0 and len(items['us']) != 0:
            print('英:', items['uk'][0], ' 美:', items['us'][0])
        else:
            if len(items['uk']) != 0:
                print('英:', items['uk'][0])
            else:
                print('美:', items['us'][0])
    return items


def main():
    last_data = None
    filename = get_path()+"wordlist.txt"
    wordlist = WordList(filename=filename)
    datefilename = get_path()+"datefile.txt"
    datelist = Fusion(datefilename)
    datelist.write_date_to_file()
    b_shown = False
    options, args = getopt.getopt(sys.argv, "-3-4")
    if ('-3', '')in options or '3' in args:
        random_test_hint_always(wordlist, datelist, True)
    elif ('-4', '')in options or '4' in args:
        random_test_hint_always(wordlist, datelist)
    while True:
        try:
            if ('-1', '1') in options or '1' in args:
                subprocess.Popen(get_path() + "clipboard_launcher.bat ", creationflags=subprocess.CREATE_NEW_CONSOLE)
                exit()
            elif ('-2', '2') in options or '2' in args:
                c = "2"
            else:
                show_menu()
                c = input().strip().lower()
            while len(c) == 0:
                c = input().strip().lower()
            if c == "1":
                show_word(wordlist)
                b_shown = True
            elif c == "3":
                if b_shown:
                    random_test_hint_always(wordlist, datelist, recent=True, savefile=True)
                    exit()
                else:
                    random_test_hint_always(wordlist, datelist, True)
            elif c == "4":
                if b_shown:
                    random_test_hint_always(wordlist, datelist, recent=False, savefile=True)
                    exit()
                else:
                    random_test_hint_always(wordlist, datelist)
            elif c == "5":
                fuzzy_finder(wordlist, datelist)
            elif c == "6":
                wordlist.sort_by_time()
                show_word(wordlist, show_date_delimeter=True)
            elif c == "7":
                mistake_collection(wordlist, datelist)
            elif c == "8":
                if new_word_auto_chrome(wordlist, datelist):
                    wordlist.write_wordlist_to_file()
                    datelist.write_date_to_file()
                    print("今天共录入了", datelist.today().input_count(), "个单词，加油！")
            elif c == "9":
                random_test_chn(wordlist, datelist)
            elif c == "0":
                while True:
                    show_sub_menu()
                    c = input().strip().lower()
                    while len(c) == 0:
                        c = input().strip().lower()
                    if c == "1":
                        print_graph(datelist)
                        on_progress()
                    elif c == "2":
                        statistics(wordlist, datelist)
                    elif c == "3":
                        replace_youdao(wordlist)
                    elif c == "6":
                        show_phrases(wordlist)
                    elif c == "7":
                        show_word(wordlist.get_list_today())
                    elif c == "8":
                        wordlist.sort_by_date()
                        show_word(wordlist, True)
                    elif c == "9":
                        wordlist.show_everything()                        
                    elif c == "0":
                        break
                    else:
                        impatient_search(c, wordlist, datelist)
            else:
                impatient_search(c, wordlist, datelist)
        except EOFError:
            print("无效输入，已经取消操作")
            continue


def random_test_chn(wordlist, datelist, recent=False):
    if not recent:
        p = choice(wordlist.get_unvisited_list())
    else:
        p = wordlist.get_unvisited_list(True, True)[0]
    wordlist.visit(p)
    p2 = p
    p3 = p
    print(p.it_self()),
    try:
        page_src = get_one_page("http://dict.youdao.com/w/" + p.it_self() + "/#keyfrom=dict2.index")
        get_phonetic(page_src)
    except:
        pass
    print("对应哪个中文？(输入Ctrl+C退出)")
    if len(wordlist.get_unvisited_list()) > 0:
        p2 = choice(wordlist.get_unvisited_list())
    if len(wordlist.get_unvisited_list()) > 1:
        p3 = choice(wordlist.get_unvisited_list())
        while p3 == p2:
            p3 = choice(wordlist.get_unvisited_list())
    seed = random.randint(0, 2)
    if seed == 0:
        if len(wordlist.get_unvisited_list()) == 0:
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            print("提供以下两个选择:"), print("(1)."+p.explanation()), print("(2)."+p2.explanation())
        else:
            print("提供以下三个选择:"), print("(1)."+p.explanation()), print("(2)."+p2.explanation()), print("(3)."+p3.explanation())
    elif seed == 1:
        if len(wordlist.get_unvisited_list()) == 0:
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            print("提供以下两个选择:"), print("(1)."+p2.explanation()), print("(2)."+p.explanation())
        else:
            print("提供以下三个选择:"), print("(1)."+p2.explanation()), print("(2)."+p.explanation()), print("(3)."+p3.explanation())
    elif seed == 2:
        if len(wordlist.get_unvisited_list()) == 0:
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            print("提供以下两个选择:"), print("(1)."+p.explanation()), print("(2)."+p2.explanation())
        else:
            print("提供以下三个选择:"), print("(1)."+p2.explanation()), print("(2)."+p3.explanation()), print("(3)."+p.explanation())
    ans = input().strip().lower()
    while len(ans) == 0:
        ans = input().strip().lower()
    if ans == "exit()":
        return False
    if ans == p.explanation() or ans == str(seed+1):
        if len(wordlist.get_unvisited_list()) == 0:
            print("你已经全部都答完啦！")
            test_done(p, datelist, wordlist, True)
        else:
            test_done(p, datelist, wordlist, True)
            random_test_chn(wordlist, datelist, recent)
    else:
        print("正确答案是:", p.explanation())
        test_done(p, datelist, wordlist, False)
        random_test_chn(wordlist, datelist, recent)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断执行...")
        exit()
