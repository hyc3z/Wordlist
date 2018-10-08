from importlib import import_module
import ctypes


def get_path():
    path_file = __file__
    folder_path = re.search("(.*)/", path_file)
    if folder_path is None:#
        folder_path = re.search(r"(.*)\\", path_file)#为什么要这么写呢，因为ctmd在cmd里的路径是用的反斜杠，在ide里用的是正斜杠
    return folder_path.group()


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


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


modules = ['re', 'random', 'os', 'sys', 'getopt', 'subprocess','contextlib', 'decimal', 'zipfile', 'datetime', 'copy', 'time', 'matplotlib', 'selenium', 'requests' ]
import_progress = ProgressBar("加载模块...", total=len(modules), unit="", chunk_size=1, run_status="正在加载", fin_status="加载完成")

try:
    for module in modules:
        locals()[module] = import_module(module)
        import_progress.refresh(count=1)

except ModuleNotFoundError:
    print("\n模组安装不完全，是否自动下载安装？(y/n)")
    chx = input().strip().lower()
    while len(chx) == 0:
        chx = input().strip().lower()
    if chx == 'y':
        if is_admin():
            p = subprocess.Popen("pip install selenium matplotlib requests", creationflags=subprocess.CREATE_NEW_CONSOLE)
            p.communicate()
            subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
            sys.exit()
        # 将要运行的代码加到这里
        else:
            print("您未以管理员身份运行此脚本，安装可能出现错误，是否重新以管理员身份运行？(y/n)")
            chx = input().strip().lower()
            while len(chx) == 0:
                chx = input().strip().lower()
            if chx == 'y':
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                sys.exit()
            else:
                sys.exit()
    else:
        sys.exit()
except KeyboardInterrupt:
    print("用户中断执行...")
    sys.exit()


def open_console(num=0):
    path = get_path()
    os.system("cd " + path)
    if num != 0:
        subprocess.Popen("背单词launcher.bat "+ str(num), creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen("背单词launcher.bat",  creationflags = subprocess.CREATE_NEW_CONSOLE)
    sys.exit()


try:
    from random import choice
    from requests.exceptions import RequestException
    from datetime import date
    from copy import deepcopy
    import matplotlib.pyplot as plt
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
except ModuleNotFoundError:
    print("模组安装不完全，是否自动下载安装？(y/n)")
    chx = input().strip().lower()
    while len(chx) == 0:
        chx = input().strip().lower()
    if chx == 'y':
        if is_admin():
            p = subprocess.Popen("pip install selenium matplotlib requests", creationflags=subprocess.CREATE_NEW_CONSOLE)
            p.communicate()
            subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
            sys.exit()
        # 将要运行的代码加到这里
        else:
            print("您未以管理员身份运行此脚本，安装可能出现错误，是否重新以管理员身份运行？(y/n)")
            chx = input().strip().lower()
            while len(chx) == 0:
                chx = input().strip().lower()
            if chx == 'y':
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                sys.exit()
            else:
                sys.exit()
    else:
        sys.exit()
except KeyboardInterrupt:
    print("用户中断执行...")
    sys.exit()

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
    "71": "70.0.3538.16"
}
minimum_requirement = 29
maximum_support = 71
version_lookup = {
    "v1.0.0": "背单词小py",
    "v1.0.1": """修复了录入单词hint的bug
修复了重新开始时只有一个单词的bug""",
    "v1.1.0": """加入了做题计数器和错误计数器，为以后更新错题集和统计图表准备，wordlist不再向下兼容，可用converter进行转换
加入了查找单词功能
加入了手动保存功能""",
    "v1.1.1": """修复了随机测试显示list而非中文的bug""",
    "v1.1.2": """修复了重新开始时闪退bug(函数漏写一个参数233)
完善错题统计的后台支持""",
    "v1.2.0": """增加了错题集功能（预支持版本）
现在每次做题后都能显示正确率和做题次数了""",
    "v1.3.0": "增加了智能录入功能，只需输入英文自动搜索匹配中文解释",
    "v1.3.5": """完善了爬取阶段
增加图表预支持""",
    "v1.3.6": "修复了录入单词后访问错题集报错的bug",
    "v1.3.7": "从目录中移除了chromedriver，请自行下载相应版本",
    "v1.4.0": "增加统计数据功能",
    "v1.4.2": """增加了窗口异常关闭处理方法
增加了搜索失败处理方法""",
    "v1.4.3": "增加了每日录入单词统计和每日做题统计",
    "v1.4.4": "修复了无法运行的bug",
    "v1.4.5": "显示图表更新到v1.0.1版本",
    "v1.4.6": "增加输入空格时的兼容性(strip())",
    "v1.4.7": "增加随机测试hint always版",
    "v1.4.8": "微调随机测试显示格式",
    "v1.4.9": "增加输入容错率",
    "v1.4.10": "调整提示的分隔显示方式，更容易分辨词组",
    "v1.4.11": "修复了每日做题统计无法显示的bug(其实是忘了写)",
    "v1.4.12": """增加KeyboardInterrupt处理方法
用Decimal代替表示概率
其他的一些小修改让程序更加易用""",
    "v1.5.0": """本人python的学习暂时告一段落了，此项目可能会暂停更新一段时间
v1.5.0是这个小程序的latest version，希望大家喜欢！""",
    "v1.5.2": "增加错题集测试功能",
    "v1.5.3": "增加自动下载chromedriver模块",
    "v1.6.0": """重构import部分，现在有进度条和管理员机制
增加管理员运行部分
增加下载文件的实时进度条
修复了自动查找chrome版的一些bug
将moduleInstaller整合进脚本内部""",
    "v1.6.1": "模糊本地查找",
    "v1.6.2": """将版本信息整合进脚本内部
使用pyc代替源代码发布release
修改了菜单结构""",
    "v1.6.3": "增加换行使版本信息更易读",
    "v1.6.4": "增加了自动录入的断线情况处理",
    "v1.6.5": "增加了词组和单词的区分",
    "v1.6.6": "现在在显示已经录入该单词时，会显示录入的单词解释",
    "v1.6.7": """保存文件换成utf-8格式
用自己写的get_path()代替了os.getcwd()，让脚本也可以开机运行时找到路径""",
    "v1.6.8": "用面向对象重构了wordlist, 累死爹了",
    "v1.7.0": "全部面向对象重构版本,beta版",
    "v1.7.1": "全部面向对象重构版本,RC版",
    "v1.7.2": "终于有了，所有单词词组的字母排序！",
    "v1.7.3": "加入直接在菜单搜索的功能"
}
known_issue = [
]
version_info = "v1.7.3"

class Atom:

    def __init__(self,date = str(date.today()), testedcount=0, searchcount=0, inputcount=0):
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
        print(self.__date, "录入了", self.__inputCount, "个单词, 搜索了",self.__searchCount,"题, 做了",self.__testedCount,"题")


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

    def __init__(self, enword, cnexplanation, testedcount=0, correctcount=0, searchtime=0):
        self.__enWord = enword
        self.__cnExplanation = cnexplanation
        self.__testedCount = testedcount
        self.__correctCount = correctcount
        self.__searchTime = searchtime
        self.__Visited = False

    def it_self(self):
        return self.__enWord

    def explanation(self):
        return self.__cnExplanation

    def tested_count(self):
        return self.__testedCount

    def correct_count(self):
        return self.__correctCount

    def incorrect_count(self):
        return self.__testedCount-self.__correctCount

    def correct_rate(self):
        return round(Decimal(self.__correctCount/self.__testedCount * 100.0), 2)

    def incorrect_rate(self):
        return round(Decimal((self.__testedCount-self.__correctCount) / self.__testedCount* 100.0), 2)

    def searched_count(self):
        return self.__searchTime

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
        print(self.it_self(), "已做", self.tested_count(), "次，正确", self.correct_count(), "次，正确率", self.incorrect_rate(), "%")

    def visited(self):
        return self.__Visited

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

    def init_visit_status(self):
        self.__unvisitedList = []
        for word in self.__wordList:
            if not word.visited():
                self.__unvisitedList.append(word)

    def read_wordlist_from_file(self, filename=None):
        if filename is None:
            filename = self.__filename
        try:
            fpt = {}
            f = open(filename, "r", encoding="utf-8-sig")  # qnmd \ufeff 我真的佛了
            pre_f = f.read()
            post_f = re.split('\n', pre_f)
            for i in range(1, len(post_f), 3):
                fpt[post_f[i - 1].replace("\s", "")] = [post_f[i].replace("\s", "")]
                numeric_data = post_f[i + 1].split(' ')
                for j in numeric_data:
                    fpt[post_f[i - 1].replace("\s", "")].append(j)
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
            singleword = Word(i, fpt[i][0], int(fpt[i][1]), int(fpt[i][2]), int(fpt[i][3]))
            self.__wordList.append(singleword)
            self.__engList.append(singleword.it_self())
            if singleword.is_phrase():
                self.__phraseList.append(singleword)

    def write_wordlist_to_file(self, filename=None):
        if filename is None:
            filename = self.__filename
        f = open(filename, "w+", encoding="utf-8")
        for i in self.__wordList:
            f.write(i.it_self() + "\n")
            f.write(i.explanation() + "\n")
            f.write(i.numeric_data() + "\n")
        f.close()

    def __init__(self, filename=None):
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

    def comlete_list(self):
        return self.__wordList

    def get_unvisited_list(self):
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
        newWord = Word(en_word, cn_word)
        self.__wordList.append(newWord)
        self.__unvisitedList.append(newWord)
        self.__engList.append(newWord.it_self())
        if newWord.is_phrase():
            self.__phraseList.append(newWord)

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

    def sort_by_alphabet(self):
        self.__wordList = sorted(self.__wordList, key=lambda x: x.it_self())


def show_menu():
    if is_admin():
        print("背单词", version_info, " 管理员模式", date_today)
    else:
        print("背单词", version_info, " 用户模式", date_today)
    print("1:显示所有单词和词组")
    print("2:人工录入")
    print("3:随机测试")
    print("4:随机测试hint always版")
    print("5:本地模糊查找单词")
    print("6:手动保存")
    print("7:错题集")
    print("8:自动录入chrome版")
    print("9:自动录入requests版")
    print("0:其他功能")


def show_sub_menu():
    if is_admin():
        print("背单词", version_info, " 管理员模式", date_today)
    else:
        print("背单词", version_info, " 用户模式", date_today)
    print("1:显示图表")
    print("2:统计数据")
    print("3:把所有单词及词组替换成有道词典版本")
    print("4:显示当前版本信息")
    print("5:显示所有历史版本信息")
    print("6:显示所有词组")
    if not is_admin():
        print("admin:以管理员模式重新启动")
    print("0:返回主菜单")


def on_progress():
    print("该功能还在开发中！")


def test_done(p, datelist, wordlist, correct=False):
    if correct:
        p.correct()
    else:
        p.incorrect()
    datelist.today().tested()
    datelist.write_date_to_file()
    p.show_rate()
    wordlist.write_wordlist_to_file()


def statistics(wordlist, datelist):
    print("共有", len(wordlist), "个单词及词组收录。")
    for i in datelist:
        i.show_info()
    print()
    datelist.searched_most(show=True)
    datelist.input_most(show=True)
    datelist.tested_most(show=True)
    print("\n今天：")
    datelist.today().show_info()
    os.system("pause")


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
        random_test_hint_always(soup, datelist)
    return soup


def random_test(wordlist, datelist):
    p = choice(wordlist.get_unvisited_list())
    p.visit()
    p2 = p
    p3 = p
    egg = False
    print(p.explanation(), " 对应哪个单词？(输入hint得到提示，输入Ctrl+C退出)")
    ans = input().strip().lower()
    while len(ans) == 0:
        ans = input().strip().lower()
    if p.it_self() == "hint":
        egg = True
    if ans == "exit()":
        return False
    if ans == "hint" and not egg:
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
                print("提供以下两个选择:", p.it_self(), ",", p2.it_self())
            else:
                print("提供以下三个选择:", p.it_self(), ",", p2.it_self(), ",", p3.it_self())
        elif seed == 1:
            if len(wordlist.get_unvisited_list()) == 0:
                print("只有一个单词了！")
            elif len(wordlist.get_unvisited_list()) == 1:
                print("提供以下两个选择:", p2.it_self(), ",", p.it_self())
            else:
                print("提供以下三个选择:", p2.it_self(), ",", p.it_self(), ",", p3.it_self())
        elif seed == 2:
            if len(wordlist.get_unvisited_list()) == 0:
                print("只有一个单词了！")
            elif len(wordlist.get_unvisited_list()) == 1:
                print("提供以下两个选择:", p.it_self(), ",", p2.it_self())
            else:
                print("提供以下三个选择:", p2.it_self(), ",", p3.it_self(), ",", p.it_self())
        ans = input().strip().lower()
        while len(ans) == 0:
            ans = input().strip().lower()
    if ans == p.it_self():
        if len(wordlist.get_unvisited_list()) == 0:
            if not egg:
                print("你已经全部都答完啦！重新开始吗？(Y/N)")
                test_done(p, datelist, wordlist, True)
                chx = input().strip().lower()
                while len(chx) == 0:
                    chx = input().strip().lower()
                if chx == "Y" or chx == "y":
                    open_console(3)
                else:
                    open_console()
            else:
                print('''Traceback (most recent call last):
                  File "C:/PycharmProjects/背单词/背单词.py", line 176, in <module>
                    main(sys.argv[1:])
                  File "C:/PycharmProjects/背单词/背单词.py", line 171, in main
                    if random_test(quiz_cache):
                  File "C:/PycharmProjects/背单词/背单词.py", line 98, in random_test
                    print("Error: hint",hint)
                NameError: name 'hint' != defined''')
                time.sleep(2)
                print("提示:上面的报错是骗你的，输入(Y/N)进入下一题吧！")
                test_done(p, datelist, wordlist, True)
                chx = input().strip().lower()
                while len(chx) == 0:
                    chx = input().strip().lower()
                if chx == "Y" or chx == "y":
                    open_console(3)
                else:
                    open_console()
        else:
            if not egg:
                test_done(p, datelist, wordlist, True)
                random_test(wordlist, datelist)
            else:
                print(r'''Traceback (most recent call last):
  File "C:/PycharmProjects/背单词/背单词.py", line 176, in <module>
    main(sys.argv[1:])
  File "C:/PycharmProjects/背单词/背单词.py", line 171, in main
    if random_test(quiz_cache):
  File "C:/PycharmProjects/背单词/背单词.py", line 98, in random_test
    print("Error: hint",hint)
NameError: name 'hint' != defined''')
                time.sleep(2)
                print("提示：上面的报错是骗你的，输入(Y/N)进入下一题吧！")
                test_done(p, datelist, wordlist, True)
                chs = input().strip().lower()
                while len(chs) == 0:
                    chs = input().strip().lower()
                if chs == "Y" or chs == "y":
                    random_test(wordlist, datelist)
                else:
                    return False
    else:
        print("正确答案是:", p.it_self())
        print("还敢来吗?(Y/N)")
        test_done(p, datelist, wordlist, False)
        chs = input().strip().lower()
        while len(chs) == 0:
            chs = input().strip().lower()
        if len(wordlist.get_unvisited_list()) == 0:
            if chs == "Y" or chs == "y":
                open_console(3)
            else:
                open_console()
        else:
            if chs == "Y" or chs == "y":
                random_test(wordlist, datelist)
            else:
                return False


def random_test_hint_always(wordlist, datelist):
    p = choice(wordlist.get_unvisited_list())
    wordlist.visit(p)
    p2 = p
    p3 = p
    print(p.explanation(), " 对应哪个单词？(输入Ctrl+C退出)")
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
            print("提供以下两个选择:", p.it_self(), ",", p2.it_self())
        else:
            print("提供以下三个选择:", p.it_self(), ",", p2.it_self(), ",", p3.it_self())
    elif seed == 1:
        if len(wordlist.get_unvisited_list()) == 0:
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            print("提供以下两个选择:", p2.it_self(), ",", p.it_self())
        else:
            print("提供以下三个选择:", p2.it_self(), ",", p.it_self(), ",", p3.it_self())
    elif seed == 2:
        if len(wordlist.get_unvisited_list()) == 0:
            print("只有一个单词了！")
        elif len(wordlist.get_unvisited_list()) == 1:
            print("提供以下两个选择:", p.it_self(), ",", p2.it_self())
        else:
            print("提供以下三个选择:", p2.it_self(), ",", p3.it_self(), ",", p.it_self())
    ans = input().strip().lower()
    while len(ans) == 0:
        ans = input().strip().lower()
    if ans == "exit()":
        return False
    if ans == p.it_self():
        if len(wordlist.get_unvisited_list()) == 0:
            print("你已经全部都答完啦！重新开始吗？(Y/N)")
            test_done(p, datelist, wordlist, True)
            chx = input().strip().lower()
            while len(chx) == 0:
                chx = input().strip().lower()
            if chx == "Y" or chx == "y":
                open_console(4)
            else:
                open_console()
        else:
            test_done(p, datelist, wordlist, True)
            random_test_hint_always(wordlist, datelist)
    else:
        print("正确答案是:", p.it_self())
        print("还敢来吗?(Y/N)")
        test_done(p, datelist, wordlist, False)
        chs = input().strip().lower()
        while len(chs) == 0:
            chs = input().strip().lower()
        if len(wordlist.get_unvisited_list()) == 0:
            if chs == "Y" or chs == "y":
                open_console(4)
            else:
                open_console()
        else:
            if chs == "Y" or chs == "y":
                random_test_hint_always(wordlist, datelist)
            else:
                return False


def new_word(wordlist, datelist):
    print("输入英文:(输入 Ctrl+C 取消录入)")
    word = input().strip().lower()
    while len(word) == 0:
        word = input().strip().lower()
    result = wordlist.search(word)
    while result is not None:
        print(result.it_self(), result.explanation())
        print(word, "已经存在，请重新输入")
        word = input().strip().lower()
        while len(word) == 0:
            word = input().strip().lower()
        if word == "exit()":
            print("已取消录入")
            return False
        result = wordlist.search(word)
    print("输入中文：(输入 Ctrl+C 取消录入)")
    word_cn = input().strip().lower()
    while len(word_cn) == 0:
        word_cn = input().strip().lower()
    if word_cn == "exit()":
        print("已取消录入")
        return False
    word_cnt = word.split(' ')
    if len(word_cnt) is 1:
        print(word, word_cn, "确认把这个单词加入列表吗?(Y/N)")
    else:
        print(word, word_cn, "确认把这个词组加入列表吗?(Y/N)")
    cfm = input().strip().lower()
    while len(cfm) == 0:
        cfm = input().strip().lower()
    if cfm == "Y" or cfm == "y":
        wordlist.add_new_word(word, word_cn)
        datelist.today().grow()
        return True
    else:
        print("已取消录入")
        return False


def get_cur_ver_info(cur_ver):
    return version_lookup[cur_ver]


def get_all_versions():
    for i in version_lookup:
        print(i)
        print(version_lookup[i])
        print()
    print("共", len(version_lookup), "个版本")
    os.system("pause")
    return version_lookup


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
                        open_console()
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
        response = requests.get(url, headers=headers)
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
    result = wordlist.search(word)
    if result is not None:
        print(word, result.explanation())
        datelist.today().searched()
        result.searched()
        wordlist.write_wordlist_to_file()
        datelist.write_date_to_file()
        return False
    else:
        try:
            page_src = get_one_page("http://dict.youdao.com/w/eng/"+word+"/#keyfrom=dict2.index")
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


def show_word(wordlist):
    for i in wordlist:
        print(i.it_self(), i.explanation())


def show_phrases(wordlist):
    count = 0
    for i in wordlist:
        if i.is_phrase():
            print(i.it_self(),i.explanation())
            count += 1
    print("共", count, "个词组")


def display_cur_version():
    print()
    print("第", len(version_lookup), "个版本")
    print(version_info)
    print(get_cur_ver_info(version_info))
    if len(known_issue) is not 0:
        print("已知问题:")
        for i in known_issue:
            print(i)
    print()
    os.system("pause")


def main(argv):
    filename = get_path()+"\\wordlist.txt"
    wordlist = WordList(filename)
    datefilename = get_path()+"\\datefile.txt"
    datelist = Fusion(datefilename)
    datelist.write_date_to_file()
    b_shown = False
    options, args = getopt.getopt(argv, "-3-4")
    if ('-3', '')in options or '3' in args:
        random_test(wordlist, datelist)
    elif ('-4', '')in options or '4' in args:
        random_test_hint_always(wordlist, datelist)
    while True:
        try:
            show_menu()
            c = input().strip().lower()
            while len(c) == 0:
                c = input().strip().lower()
            if c == "1":
                show_word(wordlist)
                b_shown = True
            elif c == "2":
                if new_word(wordlist, datelist):
                    wordlist.write_wordlist_to_file()
                    datelist.write_date_to_file()
                    print("今天共录入了", datelist.today().input_count(), "个单词，加油！")
            elif c == "3":
                if b_shown:
                    open_console(3)
                else:
                    random_test(wordlist, datelist)
            elif c == "4":
                if b_shown:
                    open_console(4)
                else:
                    random_test_hint_always(wordlist, datelist)
            elif c == "5":
                fuzzy_finder(wordlist, datelist)

            elif c == "6":
                wordlist.write_wordlist_to_file()
                datelist.write_date_to_file()
            elif c == "7":
                mistake_collection(wordlist, datelist)
            elif c == "8":
                if new_word_auto_chrome(wordlist, datelist):
                    wordlist.write_wordlist_to_file()
                    datelist.write_date_to_file()
                    print("今天共录入了", datelist.today().input_count(), "个单词，加油！")
            elif c == "9":
                if new_word_auto_requests(wordlist, datelist):
                    wordlist.write_wordlist_to_file()
                    datelist.write_date_to_file()
                    print("今天共录入了", datelist.today().input_count(), "个单词，加油！")
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
                    elif c == "4":
                        display_cur_version()
                    elif c == "5":
                        get_all_versions()
                    elif c == "6":
                        show_phrases(wordlist)
                    elif c == "admin":
                        if is_admin():
                            print("脚本已经在管理员模式下运行！")
                        else:
                            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                            sys.exit()
                    elif c == "0":
                        break
                    else:
                        impatient_search(c, wordlist, datelist)
            else:
                impatient_search(c, wordlist, datelist)
        except EOFError:
            print("无效输入，已经取消操作")
            continue
        except KeyboardInterrupt:
            print("取消操作")
            continue


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("用户中断执行...")
