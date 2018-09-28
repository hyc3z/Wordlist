import re
from random import choice
import random
import sys
import os
import getopt
import subprocess
import time
from copy import deepcopy
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException


def read(filename):
    f = open(filename, "r")
    strn = f.read()
    fpt = {}
    res = re.split('\n', strn)
    for i in range(1, len(res), 4):
        fpt[res[i-1]] = [res[i], int(res[i+1]), int(res[i+2]), int(res[i+1])-int(res[i+2])]
    f.close()
    return fpt


def read_date(filename):
    f = open(filename, "r")
    strn = f.read()
    fpt = {}
    res = re.split('\n', strn)
    for i in range(1, len(res), 3):
        fpt[res[i - 1]] = [int(res[i]), int(res[i+1])]
    f.close()
    return fpt


def write_date(filename, b):
    f = open(filename, "w+")
    for i in b:
        f.write(i + "\n")
        f.write(str(b[i][0]) + '\n')
        f.write(str(b[i][1]) + '\n')
    f.close()


def write(filename, a):
    f = open(filename, "w+")
    for i in a:
        f.write(i+"\n")
        f.write(a[i][0] + "\n" + str(a[i][1]) + '\n' + str(a[i][2]) + '\n')
    f.close()


def show_menu():
    print("背单词v1.4.11")
    print("1:显示所有单词")
    print("2:录入新单词")
    print("3:随机测试")
    print("4:随机测试hint always版")
    print("5:查找单词")
    print("6:手动保存")
    print("7:错题集")
    print("8:智能录入")
    print("9:显示图表v1.0.1")
    print("0:统计数据")


def on_progress():
    print("该功能还在开发中！")


def statistics(a, cur_date, b):
    print("共有", len(a), "个单词收录。")
    for i in b:
        print(i, "录入了", b[i][0], "个单词", "做了", b[i][1], "题")
    print("\n今天录入了", b[cur_date][0], "个单词", "做了", b[cur_date][1], "题")
    os.system("pause")


def print_graph(b):
    names = []
    values_total = []
    values_incorrect = []
    for i in b:
        names.append(i)
        values_total.append(b[i][0])
        values_incorrect.append(b[i][1])
    plt.plot(names, values_total, '-', label="Input Count")
    plt.plot(names, values_incorrect, '-', label="Quiz Count")
    plt.legend()
    plt.suptitle('in development...')
    plt.show()


def mistake_collection(wordlist):
    soup = []
    for i in wordlist:
        if (wordlist[i][1]-wordlist[i][2]) > 0:
            soup.append([i, wordlist[i][1], wordlist[i][1]-wordlist[i][2]])
    soup.sort(key=lambda x: float(x[2])/float(x[1]), reverse=True)
    return soup


def find_word(wordlist):
    print("输入查找的单词：")
    a = input().strip()
    while len(a) == 0:
        a = input().strip()
    if a in wordlist:
        print(a, wordlist[a][0])
    else:
        print("未录入该单词")


def random_test(a, wordlist, filename, b, cur_date, datefile):
    p = choice(list(a))
    p2 = p
    p3 = p
    egg = False
    print(a[p][0], " 对应哪个单词？(输入hint得到提示，输入exit()退出)")
    ans = input().strip()
    while len(ans) == 0:
        ans = input().strip()
    if p == "hint":
        egg = True
    if ans == "exit()":
        return False
    if ans == "hint" and not egg:
        while p2 == p and len(a) > 1:
            p2 = choice(list(a))
        while (p3 == p2 or p3 == p) and len(a) > 2:
            p3 = choice(list(a))
        seed = random.randint(0, 2)
        if seed == 0:
            if len(a) == 1:
                print("只有一个单词了！")
            elif len(a) == 2:
                print("提供以下两个选择:", p, ",", p2)
            else:
                print("提供以下三个选择:", p, ",", p2, ",", p3)
        elif seed == 1:
            if len(a) == 1:
                print("只有一个单词了！")
            elif len(a) == 2:
                print("提供以下两个选择:", p2, ",", p)
            else:
                print("提供以下三个选择:", p2, ",", p, ",", p3)
        elif seed == 2:
            if len(a) == 1:
                print("只有一个单词了！")
            elif len(a) == 2:
                print("提供以下两个选择:", p, ",", p2)
            else:
                print("提供以下三个选择:", p2, ",", p3, ",", p)
        ans = input().strip()
        while len(ans) == 0:
            ans = input().strip()
    if ans == p:
        if len(a) == 1:
            if not egg:
                print("你已经全部都答完啦！重新开始吗？(Y/N)")
                wordlist[p][1] += 1
                wordlist[p][2] += 1
                b[cur_date][1] += 1
                write_date(datefile, b)
                print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率", round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
                write(filename, wordlist)
                chx = input()
                if chx == "Y" or chx == "y":
                    path = os.getcwd()
                    os.system("cd " + path)
                    subprocess.Popen("背单词launcher.bat -3", creationflags=subprocess.CREATE_NEW_CONSOLE)
                    sys.exit()
                else:
                    path = os.getcwd()
                    os.system("cd " + path)
                    subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
                    sys.exit()
            else:
                print('''Traceback (most recent call last):
                  File "C:/PycharmProjects/背单词/背单词.py", line 176, in <module>
                    main(sys.argv[1:])
                  File "C:/PycharmProjects/背单词/背单词.py", line 171, in main
                    if random_test(quiz_cache):
                  File "C:/PycharmProjects/背单词/背单词.py", line 98, in random_test
                    print("Error: hint",hint)
                NameError: name 'hint' is not defined''')
                time.sleep(2)
                print("提示:上面的报错是骗你的，输入(Y/N)进入下一题吧！")
                wordlist[p][1] += 1
                wordlist[p][2] += 1
                b[cur_date][1] += 1
                write_date(datefile, b)
                print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                      round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
                write(filename, wordlist)
                chx = input()
                if chx == "Y" or chx == "y":
                    path = os.getcwd()
                    os.system("cd " + path)
                    subprocess.Popen("背单词launcher.bat -3", creationflags=subprocess.CREATE_NEW_CONSOLE)
                    sys.exit()
                else:
                    path = os.getcwd()
                    os.system("cd " + path)
                    subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
                    sys.exit()
        else:
            if not egg:
                del a[p]
                wordlist[p][1] += 1
                wordlist[p][2] += 1
                b[cur_date][1] += 1
                write_date(datefile, b)
                print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                      round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
                write(filename, wordlist)
                random_test(a, wordlist, filename, b, cur_date, datefile)
            else:
                print(r'''Traceback (most recent call last):
  File "C:/PycharmProjects/背单词/背单词.py", line 176, in <module>
    main(sys.argv[1:])
  File "C:/PycharmProjects/背单词/背单词.py", line 171, in main
    if random_test(quiz_cache):
  File "C:/PycharmProjects/背单词/背单词.py", line 98, in random_test
    print("Error: hint",hint)
NameError: name 'hint' is not defined''')
                time.sleep(2)
                print("提示：上面的报错是骗你的，输入(Y/N)进入下一题吧！")
                wordlist[p][1] += 1
                wordlist[p][2] += 1
                b[cur_date][1] += 1
                write_date(datefile, b)
                print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                      round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
                write(filename, wordlist)
                chs = input()
                if chs == "Y" or chs == "y":
                    del a[p]
                    random_test(a, wordlist, filename, b, cur_date, datefile)
                else:
                    return False
    else:
        print("正确答案是:", p)
        print("还敢来吗?(Y/N)")
        wordlist[p][1] += 1
        wordlist[p][2] += 0
        b[cur_date][1] += 1
        write_date(datefile, b)
        print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
              round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
        write(filename, wordlist)
        chs = input()
        if len(a) == 1:
            if chs == "Y" or chs == "y":
                path = os.getcwd()
                os.system("cd " + path)
                subprocess.Popen("背单词launcher.bat -3", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
            else:
                path = os.getcwd()
                os.system("cd " + path)
                subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
        else:
            if chs == "Y" or chs == "y":
                random_test(a, wordlist, filename, b, cur_date, datefile)
            else:
                return False


def random_test_hint_always(a, wordlist, filename, b, cur_date, datefile):
    p = choice(list(a))
    p2 = p
    p3 = p
    print(a[p][0], " 对应哪个单词？(输入exit()退出)")
    while p2 == p and len(a) > 1:
        p2 = choice(list(a))
    while (p3 == p2 or p3 == p) and len(a) > 2:
        p3 = choice(list(a))
    seed = random.randint(0, 2)
    if seed == 0:
        if len(a) == 1:
            print("只有一个单词了！")
        elif len(a) == 2:
            print("提供以下两个选择:", p, ",", p2)
        else:
            print("提供以下三个选择:", p, ",", p2, ",", p3)
    elif seed == 1:
        if len(a) == 1:
            print("只有一个单词了！")
        elif len(a) == 2:
            print("提供以下两个选择:", p2, ",", p)
        else:
            print("提供以下三个选择:", p2, ",", p, ",", p3)
    elif seed == 2:
        if len(a) == 1:
            print("只有一个单词了！")
        elif len(a) == 2:
            print("提供以下两个选择:", p, ",", p2)
        else:
            print("提供以下三个选择:", p2, ",", p3, ",", p)
    ans = input().strip()
    while len(ans) == 0:
        ans = input().strip()
    if ans == "exit()":
        return False
    if ans == p:
        if len(a) == 1:
            print("你已经全部都答完啦！重新开始吗？(Y/N)")
            wordlist[p][1] += 1
            wordlist[p][2] += 1
            b[cur_date][1] += 1
            write_date(datefile, b)
            print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率", round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
            write(filename, wordlist)
            chx = input()
            if chx == "Y" or chx == "y":
                path = os.getcwd()
                os.system("cd " + path)
                subprocess.Popen("背单词launcher.bat -4", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
            else:
                path = os.getcwd()
                os.system("cd " + path)
                subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
        else:
            del a[p]
            wordlist[p][1] += 1
            wordlist[p][2] += 1
            b[cur_date][1] += 1
            write_date(datefile, b)
            print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                  round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
            write(filename, wordlist)
            random_test_hint_always(a, wordlist, filename, b, cur_date, datefile)
    else:
        print("正确答案是:", p)
        print("还敢来吗?(Y/N)")
        wordlist[p][1] += 1
        wordlist[p][2] += 0
        b[cur_date][1] += 1
        write_date(datefile, b)
        print(p, "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
              round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%", '\n')
        write(filename, wordlist)
        chs = input()
        if len(a) == 1:
            if chs == "Y" or chs == "y":
                path = os.getcwd()
                os.system("cd " + path)
                subprocess.Popen("背单词launcher.bat -4", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
            else:
                path = os.getcwd()
                os.system("cd " + path)
                subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
        else:
            if chs == "Y" or chs == "y":
                random_test_hint_always(a, wordlist, filename, b, cur_date, datefile)
            else:
                return False


def new_word(a, cur_date, b):
    print("输入英文:(输入 'exit()' 取消录入)")
    word = input().strip()
    while len(word) == 0:
        word = input().strip()
    if word == "exit()":
        print("已取消录入")
        return False
    if word in a:
        print(word, "已经存在，请重新输入")
        word = input().strip()
        while len(word) == 0:
            word = input().strip()
        if word == "exit()":
            print("已取消录入")
            return False
    print("输入中文：(输入 'exit()' 取消录入)")
    word_cn = input().strip()
    while len(word_cn) == 0:
        word_cn = input().strip()
    if word_cn == "exit()":
        print("已取消录入")
        return False
    print(word, word_cn, "确认把这个单词加入列表吗?(Y/N)")
    cfm = input()
    if cfm == "Y" or cfm == "y":
        a[word] = [word_cn, 0, 0]
        b[cur_date][0] += 1
        return True
    else:
        print("已取消录入")
        return False


def new_word_auto(a, cur_date, b):
    print("输入英文:(输入 'exit()' 取消录入)")
    word = input().strip()
    while len(word) == 0:
        word = input().strip()
    if word == "exit()":
        print("已取消录入")
        return False
    if word in a:
        print(word, "已经存在，请重新输入")
        word = input().strip()
        while len(word) == 0:
            word = input().strip()
        if word == "exit()":
            print("已取消录入")
            return False
    word_cn = ""
    try:
        browser0 = webdriver.Chrome()
        wait = WebDriverWait(browser0, 5)
        browser0.get("https://www.baidu.com/")
        browser0.find_element_by_id("kw").send_keys(word)
        browser0.find_element_by_id("su").click()
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'op_dict3_english_result_table')))
        except TimeoutException:
            print("加载失败，未搜索到相关信息，尝试手动录入")
            return False
        # word_attributes = browser0.find_element_by_css_selector("span.op_dict_text1.c-gap-right")
        # word_translates = browser0.find_element_by_css_selector("span.op_dict_text2")
        word_result = browser0.find_elements_by_class_name("op_dict3_english_result_table")
        # for i in word_attributes and j in word_translates:
        #     print(i+j)
        #     word_cn = i+j

        for i in word_result:
            word_cn += i.text
        word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
        browser0.close()
        print(word, word_cn_complete, "确认把这个单词加入列表吗?(Y/N)")
        cfm = input()
        if cfm == "Y" or cfm == "y":
            a[word] = [word_cn_complete, 0, 0]
            b[cur_date][0] += 1
            return True
        else:
            print("已取消录入")
            return False
    except NoSuchWindowException:
        print("窗口异常关闭，无法继续操作。")
    except WebDriverException:
        print("引擎异常，无法继续操作。")
        return False


def show_word(a):
    for i in a:
        print(i, a[i][0])


def main(argv):
    filename = "wordlist.txt"
    a = read(filename)
    datefile = "datefile.txt"
    b = read_date(datefile)
    cur_date = str(time.strftime('%Y-%m-%d', time.localtime()))
    if cur_date not in b:
        b[cur_date] = [0, 0]
    write_date(datefile, b)
    quiz_cache = deepcopy(a)
    b_shown = False
    options, args = getopt.getopt(argv, "-3-4")
    if ('-3', '')in options or '3' in args:
        random_test(quiz_cache, a, filename, b, cur_date, datefile)
    elif ('-4', '')in options or '4' in args:
        random_test_hint_always(quiz_cache, a, filename, b, cur_date, datefile)
    while True:
        show_menu()
        c = str(input())
        if c == "1":
            show_word(a)
            b_shown = True
        elif c == "2":
            if new_word(a, cur_date, b):
                write(filename, a)
                write_date(datefile, b)
                print("今天共录入了", b[cur_date][0], "个单词，加油！")
        elif c == "3":
            if b_shown:
                path = os.getcwd()
                os.system("cd "+path)
                subprocess.Popen("背单词launcher.bat -3", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
            else:
                random_test(quiz_cache, a, filename, b, cur_date, datefile)
        elif c == "4":
            if b_shown:
                path = os.getcwd()
                os.system("cd "+path)
                subprocess.Popen("背单词launcher.bat -4", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
            else:
                random_test_hint_always(quiz_cache, a, filename, b, cur_date, datefile)
        elif c == "5":
            find_word(a)
        elif c == "6":
            write(filename, a)
        elif c == "7":
            mistake_notebook = mistake_collection(a)
            for i in mistake_notebook:
                print(i[0], "做了", i[1], "次，错了", i[2], "次，错误率", round(float(i[2])/float(i[1])*100, 2), "%")
        elif c == "8":
            if new_word_auto(a, cur_date, b):
                write(filename, a)
                write_date(datefile, b)
                print("今天共录入了", b[cur_date][0], "个单词，加油！")
        elif c == "9":
            print_graph(b)
            on_progress()
        elif c == "0":
            statistics(a, cur_date, b)
        else:
            on_progress()


if __name__ == '__main__':
    main(sys.argv[1:])
