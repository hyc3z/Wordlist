import os
import re
import requests
import pyperclip
from requests import RequestException
import time
from datetime import date
import datetime
import string
import sqlite3
import sys

date_today = str(date.today())

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

    def __init__(self, source="file", filename=None, sqlite_dbname = None):
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
                    self.__method = "file"
                else:
                    self.__wordList = []
                    self.__engList = []
                    self.__unvisitedList = []
                    self.__phraseList = []
                    self.read_from_sqlite(db_name=sqlite_dbname)
                    self.db_name=sqlite_dbname
                    self.__method = "db"


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
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        finished_count = 0
        total_count=1
        migrate_progress = ProgressBar("同步数据至数据库...", total=total_count, unit="", chunk_size=1, run_status="正在同步",
                                      fin_status="同步完成")
        if method == "searched":
            sql = """UPDATE "wordlist" SET "SEARCHED_TIMES" = "SEARCHED_TIMES"+1 WHERE "ENGLISH" = '"""+word.it_self()+"'"
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
        # def __init__(self, enword, cnexplanation, testedcount=0, correctcount=0, searchtime=0, recordedtime=str(datetime.datetime.now())):
        for word in self.__wordList:
            print(word.it_self(), word.explanation())
            print("录入时间：", word.recorded_time())
            print("做了:", word.tested_count(), "次", "对了:", word.correct_count(), "次", "搜过", word.searched_count(),"次")


def parse_one_page(document):
    pattern = re.compile('''<div class="trans-container">\s*?<ul>\s*(.*?)\s*?</ul>''', re.S)
    items1 = re.search(pattern, document)
    pattern2 = re.compile("<li>(.*?)</li>", re.S)
    if items1 is not None:
        items = re.findall(pattern2, items1.group())
    else:
        items = None
    return items

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


def get_one_page(url, max_retry=3):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        session = requests.session()
        retry_count = 1
        response = None
        while retry_count < max_retry+1:
            try:
                response = session.get(url, headers=headers, timeout=(3, 3))
                break
            except RequestException:
                print("连接词库超时... 重试中", retry_count)
                retry_count += 1
        if response is None:
            raise RequestException
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return
    except RequestException:
        raise RequestException


def impatient_search(word, wordlist):
    method = wordlist.method()
    word = word.strip().lower()#in version v 1.7.4
    result = wordlist.search(word)
    if result is not None:
        page_src = get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index")
        get_phonetic(page_src)
        print(word, result.explanation(), " 已经录入本地词库")
        result.searched()
        if method == "db":
            wordlist.update_db(method="searched", word=result)
        else:
            wordlist.write_wordlist_to_file()
        return False
    else:
        page_src = get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index")
        word_cn = ""
        items = parse_one_page(page_src)
        if items is None:
            print("有道词典未找到", word)
            return
        for i in items:
            word_cn += i
        word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
        word_cnt = word.split(' ')
        get_phonetic(page_src)
        if len(word_cnt) is 1:
            print(word, word_cn_complete, "要把这个单词加入列表吗?(Y/N)")
        else:
            print(word, word_cn_complete, "要把这个词组加入列表吗?(Y/N)")
        while True:
            cfm = input()
            if cfm == "Y" or cfm == "y":
                wordlist.add_new_word(word, word_cn_complete, save_to_sqlite=(method == "db"))
                return True
            elif cfm == "N" or cfm == "n":
                print("已取消录入")
                return False
            else:
                print("请输入正确选项！")
                continue


def monitor_clipboard(last_data, wordlist):
    clip_data = ""
    repeat = False
    fail_limit=3
    while True:
        try:
            last_data = clip_data
            fail_count = 0
            time.sleep(0.5)
            if len(pyperclip.paste())!=0:
                clip_data = pyperclip.paste()
                clip_data = clip_data.strip(string.punctuation)
                clip_data = clip_data.replace('-\n', '')
            else:
                if len(clip_data) == 0:
                    continue
            if clip_data != last_data or repeat:
                if repeat:
                    fail_count += 1
                    os.system('wifi off')
                    time.sleep(2)
                    os.system('wifi on')
                    flag = 0
                    while(flag<5):
                        try:
                            time.sleep(1)
                            ip = 'www.baidu.com'
                            backinfo = os.system('ping -c 1 -w 1 %s' % ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
                            if backinfo:
                                flag += 1
                                continue
                            else:
                                repeat = False
                                break
                        except:
                            flag += 1
                            continue
                    if fail_count == fail_limit:
                        print('Reached maximum fail count', fail_limit,', aborted.')
                        continue
                pattern = re.compile("([^a-zA-Z0-9 \-']+)", re.S)
                filtered_word = re.findall(pattern, clip_data)
                if len(filtered_word) is 0 and len(clip_data) > 1:
                    try:
                        impatient_search(clip_data, wordlist)
                        repeat = False
                        pass
                    except RequestException:
                        repeat = True
                else:
                    print("跳过无效信息")
                continue
        except TypeError:
            continue
        except KeyboardInterrupt:
            exit()


def main():
    wordlist = WordList(sqlite_dbname=os.path.join(sys.path[0], 'wordlist.db'))
    last_data = None
    monitor_clipboard(last_data, wordlist)


if __name__ == '__main__':
    try:
        print('ClipboardForLinux build v0.0.4')
        main()
    except KeyboardInterrupt:
        print("用户中断执行...")
        exit()
