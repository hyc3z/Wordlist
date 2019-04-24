import sqlite3
import re
import datetime
from datetime import date
from _word import Word
import os
import sys
from progressbar import ProgressBar

date_today = str(date.today())

class WordList:
    __wordList = []
    __engList = []
    __unvisitedList = []
    __phraseList = []
    __recentList = []

    def method(self):
        return self.__method

    def init_visit_status(self):
        self.__unvisitedList = []
        for word in self.__wordList:
            if not word.visited():
                self.__unvisitedList.append(word)

    def create_sqlite(self, db_name, table_name="wordlist"):
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS """+ table_name +""" (
                         ENGLISH  VARCHAR(100) NOT NULL,
                         CHINESE  VARCHAR(300) NOT NULL,
                         TESTED_COUNT INT,
                         CORRECT_COUNT INT,
                         SEARCHED_TIMES INT,
                         RECORDED_TIME CHAR(30) NOT NULL,
                         VISITED BOOLEAN)"""
        cursor.execute(sql)
        self.save_to_sqlite(wordlist=self.__wordList, db_name=db_name)
        db.close()


    def read_from_sqlite(self, db_name, table_name="wordlist"):
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        finished_count = 0
        sql_read = """SELECT t.* FROM """ + table_name + " t"
        q = cursor.execute(sql_read)
        query = q.fetchall()
        total_count = len(query)
        migrate_progress = ProgressBar("从数据库读取数据...", total=total_count, unit="", chunk_size=1, run_status="正在同步",fin_status="同步完成")
        for i in query:
            self.add_Word(Word(enword=i[0],cnexplanation=i[1],testedcount=i[2],correctcount=i[3],searchtime=i[4],recordedtime=i[5]))
            finished_count += 1
            migrate_progress.refresh(count=1)
        # 关闭数据库连接
        db.close()

    def save_to_sqlite(self, wordlist, db_name, table_name="wordlist"):
        # password = input("password:") # ide usage
        if db_name is None:
            db = sqlite3.connect(self.db_name)
        else:
            db = sqlite3.connect(db_name)
        cursor = db.cursor()
        finished_count = 0
        total_count = len(wordlist)
        migrate_progress = ProgressBar("同步数据至数据库...", total=total_count, unit="", chunk_size=1, run_status="正在同步",
                                      fin_status="同步完成")
        for word in wordlist:
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
            f = open(filename, "r", encoding="utf-8")  # qnmd \ufeff 我真的佛了
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
            self.add_Word(singleword)

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

    def __init__(self, filename=None, sqlite_dbname = None):
            if filename is not None:
                self.__wordList = []
                self.__engList = []
                self.__unvisitedList = []
                self.__phraseList = []
                self.__filename = filename
                self.read_wordlist_from_file(filename)
                self.init_visit_status()
                self.sort_by_alphabet()
                self.__method = "file"
            else:
                if sqlite_dbname is not None:
                    self.__wordList = []
                    self.__engList = []
                    self.__unvisitedList = []
                    self.__phraseList = []
                    self.read_from_sqlite(db_name=sqlite_dbname)
                    self.db_name=sqlite_dbname
                    self.__method = "db"
                else:
                    self.__wordList = []
                    self.__engList = []
                    self.__unvisitedList = []
                    self.__phraseList = []
                    self.__method = "arbitrary"


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

    def update_db(self, method, word):
        try:
            db = sqlite3.connect(self.db_name)
        except AttributeError:
            db = sqlite3.connect(os.path.join(sys.path[0], 'wordlist.db'))
        cursor = db.cursor()
        finished_count = 0
        total_count=1
        migrate_progress = ProgressBar("同步数据至数据库...", total=total_count, unit="", chunk_size=1, run_status="正在同步",
                                      fin_status="同步完成")
        if method == "searched":
            sql = """UPDATE "wordlist" SET "SEARCHED_TIMES" = "SEARCHED_TIMES"+1 WHERE "ENGLISH" = '"""+word.it_self()+"'"
        elif method == "test_correct":
            sql = """UPDATE "wordlist" SET "TESTED_COUNT" = "TESTED_COUNT"+1,"CORRECT_COUNT" ="CORRECT_COUNT"+1 WHERE "ENGLISH" = '"""+word.it_self()+"'"
        elif method == "test_wrong":
            sql = """UPDATE "wordlist" SET "TESTED_COUNT" = "TESTED_COUNT"+1,"CORRECT_COUNT" ="CORRECT_COUNT"+1 WHERE "ENGLISH" = '"""+word.it_self()+"'"
        else:
            sql = ""
        try:
            cursor.execute(sql)
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
        return "python?"

    def search(self, en_word):
        for word in self.__wordList:
            if word.it_self() == en_word:
                return word
        return None

    def add_new_word(self, en_word, cn_word, save_to_sqlite=True, table_name='wordlist'):
        newWord = Word(en_word, cn_word, recordedtime=str(datetime.datetime.now()))
        self.__wordList.append(newWord)
        self.__unvisitedList.append(newWord)
        self.__engList.append(newWord.it_self())
        if newWord.is_phrase():
            self.__phraseList.append(newWord)
        if save_to_sqlite:
            self.save_to_sqlite(wordlist=[newWord], db_name=self.db_name)
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
        for word in self.__wordList:
            print(word.it_self(), word.explanation())
            print("录入时间：", word.recorded_time())
            print("做了:", word.tested_count(), "次", "对了:", word.correct_count(), "次", "搜过", word.searched_count(),"次")