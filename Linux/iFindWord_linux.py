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
from _word import Word
from _wordlist import WordList
from progressbar import ProgressBar
from ifind_parse import get_one_page,parse_one_page,get_phonetic,impatient_search
from clipboard_version import get_version

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

def show_menu():
    print(get_version())
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
    print("6:显示所有词组")
    print("7:显示今日录入")
    print("8:所有单词按录入日期排序")
    print("9:显示所有单词所有信息")
    print("0:返回主菜单")


def on_progress():
    print("该功能还在开发中！")


def test_done(p, wordlist, correct=False ,savefile = True):
    if correct:
        p.correct()
        if savefile:
            wordlist.update_db(word=p, method="test_correct")
    else:
        p.incorrect()
        if savefile:
            wordlist.update_db(word=p, method="test_wrong")
    p.show_rate()


def mistake_collection(wordlist, threshold=85):
    soup = WordList()
    for i in wordlist:
        if i.incorrect_count() > 0:
            if i.correct_rate() <= threshold:
                soup.add_Word(i)
    soup.sort_by_rate()
    for i in soup:
        i.show_rate()
    print("准备好进行错题测试吗？（y/n)")
    chx = input().strip().lower()
    while len(chx) == 0:
        chx = input().strip().lower()
    if chx == 'y':
        random_test_hint_always(soup, savefile=True)
    return soup


def random_test_hint_always(wordlist, recent=False, savefile=True):
    if not recent:
        p = choice(wordlist.get_unvisited_list())
    else:
        p = wordlist.get_unvisited_list(True, True)[0]
    wordlist.visit(p)
    p2 = p
    p3 = p
    print('-'*20)
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
            test_done(p, wordlist, True, savefile)
            return
        else:
            try:
                page_src = get_one_page("http://dict.youdao.com/w/" + p.it_self() + "/#keyfrom=dict2.index")
                get_phonetic(page_src)
            except:
                pass
            test_done(p, wordlist, True, savefile)
            random_test_hint_always(wordlist, recent, savefile)
    else:
        print("正确答案是:", p.it_self())
        try:
            page_src = get_one_page("http://dict.youdao.com/w/" + p.it_self() + "/#keyfrom=dict2.index")
            get_phonetic(page_src)
        except:
            pass
        test_done(p , wordlist, False)
        random_test_hint_always(wordlist, recent, savefile)


def new_word_auto_chrome(wordlist):
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
            print("选择要录入的结果序号：(输入0退出)")
            cfm = input().strip().lower()
            while len(cfm) == 0:
                cfm = input().strip().lower()
            if cfm == "1":
                if len(word_cn_complete_baidu) != 0:
                    wordlist.add_new_word(word, word_cn_complete_baidu)
                    return True
                else :
                    print("已取消录入")
                    return False
            elif cfm == "2":
                if len(word_cn_complete_baidufanyi) != 0:
                    wordlist.add_new_word(word, word_cn_complete_baidufanyi)
                    return True
                else :
                    print("已取消录入")
                    return False
            elif cfm == "3":
                if len(word_cn_complete_youdao) != 0:
                    wordlist.add_new_word(word, word_cn_complete_youdao)
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

def fuzzy_finder(wordlist, ):
    suggestions = []
    print("输入您想查找的单词：")
    user_input = input().strip().lower()
    while len(user_input) == 0:
        user_input = input().strip().lower()
    result = wordlist.search(user_input)
    if result is not None:
        print(result.it_self(), result.explanation())
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
    wordlist = WordList(sqlite_dbname=os.path.join(sys.path[0], 'wordlist.db'))
    b_shown = False
    options, args = getopt.getopt(sys.argv, "-3-4")
    if ('-3', '')in options or '3' in args:
        random_test_hint_always(wordlist, True)
    elif ('-4', '')in options or '4' in args:
        random_test_hint_always(wordlist)
    while True:
        try:
            show_menu()
            c = input().strip().lower()
            while len(c) == 0:
                c = input().strip().lower()
            if c == "1":
                show_word(wordlist)
                b_shown = True
            elif c == "3":
                if b_shown:
                    random_test_hint_always(wordlist,  recent=True, savefile=True)
                    exit()
                else:
                    random_test_hint_always(wordlist,  True)
            elif c == "4":
                if b_shown:
                    random_test_hint_always(wordlist,  recent=False, savefile=True)
                    exit()
                else:
                    random_test_hint_always(wordlist, )
            elif c == "5":
                fuzzy_finder(wordlist, )
            elif c == "6":
                wordlist.sort_by_time()
                show_word(wordlist, show_date_delimeter=True)
            elif c == "7":
                mistake_collection(wordlist, )
            elif c == "8":
                if new_word_auto_chrome(wordlist, ):
                    wordlist.write_wordlist_to_file()
            elif c == "9":
                random_test_chn(wordlist, )
            elif c == "0":
                while True:
                    show_sub_menu()
                    c = input().strip().lower()
                    while len(c) == 0:
                        c = input().strip().lower()
                    if c == "1":
                        on_progress()
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
                        impatient_search(c, wordlist)
            else:
                impatient_search(c, wordlist, )
        except EOFError:
            print("无效输入，已经取消操作")
            continue


def random_test_chn(wordlist, recent=False):
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
            test_done(p, wordlist, True)
        else:
            test_done(p, wordlist, True)
            random_test_chn(wordlist, recent)
    else:
        print("正确答案是:", p.explanation())
        test_done(p, wordlist, False)
        random_test_chn(wordlist, recent)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断执行...")
        exit()
