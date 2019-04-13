
import re
import requests
import pyperclip
from requests import RequestException
import time
from datetime import date
import datetime
import string
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

    # def save_to_mysqldb(self, db_name="dj", table_name = "wordlist"):
    #     host = input("host:")
    #     username = input("username:")
    #     password = getpass.getpass("password:")  # console usage
    #     # password = input("password:") # ide usage
    #     db = pymysql.connect(host, username, password)
    #     cursor = db.cursor()
    #     cursor.execute("CREATE DATABASE IF NOT EXISTS "+db_name)
    #     cursor.execute("USE " + db_name)
    #     cursor.execute("DROP TABLE IF EXISTS WORDLIST")
    #     sql = """CREATE TABLE WORDLIST (
    #              ENGLISH  VARCHAR(100) NOT NULL,
    #              CHINESE  VARCHAR(300) NOT NULL,
    #              TESTED_COUNT INT,
    #              CORRECT_COUNT INT,
    #              SEARCHED_TIMES INT,
    #              RECORDED_TIME CHAR(30) NOT NULL,
    #              VISITED BOOLEAN)"""
    #     cursor.execute(sql)
    #     finished_count = 0
    #     total_count = len(self.__wordList)
    #     migrate_progress = ProgressBar("同步数据至数据库...", total=total_count, unit="", chunk_size=1, run_status="正在同步",
    #                                   fin_status="同步完成")
    #     for word in self.__wordList:
    #         sql_insert = """INSERT INTO """+table_name+"""(ENGLISH,
    #              CHINESE, TESTED_COUNT, CORRECT_COUNT, SEARCHED_TIMES, RECORDED_TIME, VISITED)
    #              VALUES (""" + word.it_self(mysql_format=True) + "," + word.explanation(mysql_format=True) + "," + \
    #                      word.tested_count(mysql_format=True) + "," + word.correct_count(mysql_format=True) + "," + \
    #                      word.searched_count(mysql_format=True) + "," + word.recorded_time(mysql_format=True) + "," + \
    #                      word.visited(mysql_format=True) + ")"
    #         try:
    #             cursor.execute(sql_insert)
    #             # 提交到数据库执行
    #             db.commit()
    #             finished_count += 1
    #             migrate_progress.refresh(count=1)
    #         except:
    #             # 如果发生错误则回滚
    #             db.rollback()
    #             print("执行第", finished_count+1, "个时发生错误。数据库已回滚")
    #             print(word)
    #     # 关闭数据库连接
    #     print(finished_count, "/", total_count, "完成")
    #     db.close()

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


def parse_one_page(document):
    pattern = re.compile('''<div class="trans-container">\s*?<ul>\s*(.*?)\s*?</ul>''', re.S)
    items1 = re.search(pattern, document)
    pattern2 = re.compile("<li>(.*?)</li>", re.S)
    items = re.findall(pattern2, items1.group())
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


def impatient_search(word, wordlist, datelist):
    word = word.strip().lower()#in version v 1.7.4
    result = wordlist.search(word)
    if result is not None:
        page_src = get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index")
        get_phonetic(page_src)
        print(word, result.explanation(), " 已经录入本地词库")
        datelist.today().searched()
        result.searched()
        wordlist.write_wordlist_to_file()
        datelist.write_date_to_file()
        return False
    else:
        page_src = get_one_page("http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.index")
        try:
            word_cn = ""
            items = parse_one_page(page_src)
            for i in items:
                word_cn += i
            word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
            word_cnt = word.split(' ')
            get_phonetic(page_src)
            if len(word_cnt) is 1:
                print(word, word_cn_complete, "要把这个单词加入列表吗?(Y/N)")
            else:
                print(word, word_cn_complete, "要把这个词组加入列表吗?(Y/N)")
            datelist.today().searched()
            while True:
                cfm = input()
                if cfm == "Y" or cfm == "y":
                    wordlist.add_new_word(word, word_cn_complete)
                    datelist.today().grow()
                    wordlist.write_wordlist_to_file()
                    datelist.write_date_to_file()
                    return True
                elif cfm == "N" or cfm == "n":
                    print("已取消录入")
                    datelist.write_date_to_file()
                    return False
                else:
                    print("请输入正确选项！")
                    continue
        except AttributeError:
            print("有道词典未找到", word, "！")


def monitor_clipboard(last_data, wordlist, datelist):
    clip_data = ""
    repeat = False
    fail_count=0
    fail_epoch=2
    fail_limit=64
    while True:
        try:
            last_data = clip_data
            time.sleep(0.2)
            if len(pyperclip.paste())!=0:
                clip_data = pyperclip.paste()
                clip_data = clip_data.strip(string.punctuation)
            else:
                if len(clip_data) == 0:
                    continue
            if clip_data != last_data or repeat:
                if repeat:
                    fail_count += 1
                    if fail_count == fail_epoch:
                        print('Retrying... ',fail_count)
                        fail_epoch *= 2
                    if fail_epoch/2 == fail_limit:
                        print('Reached maximum fail count', fail_limit,', aborted.')
                        fail_count=0
                        fail_epoch=2
                        repeat=False
                        continue
                pattern = re.compile("([^a-zA-Z0-9 \-']+)", re.S)
                filtered_word = re.findall(pattern, clip_data)
                if len(filtered_word) is 0 and len(clip_data) > 1:
                    try:
                        impatient_search(clip_data, wordlist, datelist)
                        repeat = False
                        fail_count = 0
                        fail_epoch = 2
                        pass
                    except RequestException:
                        repeat = True
                else:
                    # print("跳过无效信息:",clip_data,len(clip_data),filtered_word)
                    print("跳过无效信息")
                    # print(filtered_word)
                continue
        except TypeError:
            continue
        except KeyboardInterrupt:
            exit()


def get_path():
    path_file = __file__
    folder_path = re.search("(.*)/", path_file)
    if folder_path is None:#
        folder_path = re.search(r"(.*)\\", path_file)#为什么要这么写呢，因为ctmd在cmd里的路径是用的反斜杠，在ide里用的是正斜杠
    try:
        return folder_path.group()
    except:
        return ""


def main():
    filename = get_path()+"wordlist.txt"
    wordlist = WordList(filename=filename)
    datefilename = get_path()+"datefile.txt"
    datelist = Fusion(datefilename)
    datelist.write_date_to_file()
    last_data = None
    monitor_clipboard(last_data, wordlist, datelist)


if __name__ == '__main__':
    try:
        print('ClipboardForLinux build 20190413')
        main()
    except KeyboardInterrupt:
        print("用户中断执行...")
        exit()
