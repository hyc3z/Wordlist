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
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException

def read(filename):
    f = open(filename, "r")
    strn = f.read()
    fpt = {}
    res = re.split('\n', strn)
    for i in range(1, len(res), 4):
        fpt[res[i-1]] = [res[i], int(res[i+1]), int(res[i+2]), int(res[i+1])-int(res[i+2])]
    f.close()
    return fpt


def write(filename, a):
    f = open(filename, "w+")
    for i in a:
        f.write(i+"\n")
        f.write(a[i][0] + "\n" + str(a[i][1]) + '\n' + str(a[i][2]) + '\n')
    f.close()


def show_menu():
    print("背单词v1.4.2")
    print("1:显示所有单词")
    print("2:录入新单词")
    print("3:随机测试")
    print("4:查找单词")
    print("5:手动保存")
    print("6:错题集")
    print("7:智能录入")
    print("8:显示图表")
    print("9:统计数据")


def on_progress():
    print("该功能还在开发中！")


def statistics(a):
    print("共有", len(a), "个单词收录。")


def onpick3(event):
    ind = event.ind
    print('onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind))


def print_graph(a):
    names = []
    values_total = []
    values_incorrect = []
    for i in a:
        names.append(i)
        values_total.append(a[i][1])
        values_incorrect.append(a[i][1]-a[i][2])
    fig, q = plt.subplots()
    col = plt.plot(names, values_total, 'o', names, values_incorrect, '^', picker = True)
    fig.canvas.mpl_connect('pick_event', onpick3)
    plt.suptitle('in development...')
    plt.show()


def mistake_collection(wordlist):
    soup = []
    for i in wordlist:
        if (wordlist[i][1]-wordlist[i][2])>0:
            soup.append([i, wordlist[i][1], wordlist[i][1]-wordlist[i][2]])
    soup.sort(key=lambda x: float(x[2])/float(x[1]), reverse=True)
    return soup


def find_word(wordlist):
    a = input("输入查找的单词：")
    if a in wordlist:
        print(a, wordlist[a][0])
    else:
        print("未录入该单词")


def random_test(a, wordlist, filename):
    p = choice(list(a))
    p2 = p
    p3 = p
    egg = False
    print(a[p][0], " 对应哪个单词？(输入hint得到提示，输入exit()退出)")
    ans = input()
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
                print("提供以下两个选择:", p, p2)
            else:
                print("提供以下三个选择:", p, p2, p3)
        elif seed == 1:
            if len(a) == 1:
                print("只有一个单词了！")
            elif len(a) == 2:
                print("提供以下两个选择:", p2, p)
            else:
                print("提供以下三个选择:", p2, p, p3)
        elif seed == 2:
            if len(a) == 1:
                print("只有一个单词了！")
            elif len(a) == 2:
                print("提供以下两个选择:", p, p2)
            else:
                print("提供以下三个选择:", p2, p3, p)
        ans = input()
    if ans == p:
        if len(a) == 1:
            if not egg:
                print("你已经全部都答完啦！重新开始吗？(Y/N)")
                wordlist[p][1] += 1
                wordlist[p][2] += 1
                print(wordlist[p][0], "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率", round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%")
                write(filename, wordlist)
                chx = input()
                if chx == "Y" or chx == "y":
                    return True
                else:
                    return False
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
                print(wordlist[p][0], "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                      round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%")
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
                print(wordlist[p][0], "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                      round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%")
                write(filename, wordlist)
                random_test(a, wordlist, filename)
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
                print(wordlist[p][0], "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
                      round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%")
                write(filename, wordlist)
                chs = input()
                if chs == "Y" or chs == "y":
                    del a[p]
                    random_test(a, wordlist, filename)
                else:
                    return False
    else:
        print("正确答案是:", p)
        print("还敢来吗?(Y/N)")
        wordlist[p][1] += 1
        wordlist[p][2] += 0
        print(wordlist[p][0], "已做", wordlist[p][1], "次，正确", wordlist[p][2], "次，正确率",
              round(wordlist[p][2] / wordlist[p][1] * 100.0, 2), "%")
        write(filename, wordlist)
        chs = input()
        if chs == "Y" or chs == "y":
            random_test(a, wordlist, filename)
        else:
            return False


def new_word(a):
    print("输入英文:(输入 'exit()' 取消录入)")
    word = input()
    if word == "exit()":
        print("已取消录入")
        return False
    if word in a:
        print(word, "已经存在，请重新输入")
        word = input()
        if word == "exit()":
            print("已取消录入")
            return False
    print("输入中文：(输入 'exit()' 取消录入)")
    word_cn = input()
    if word_cn == "exit()":
        print("已取消录入")
        return False
    print(word, word_cn, "确认把这个单词加入列表吗?(Y/N)")
    cfm = input()
    if cfm == "Y" or cfm == "y":
        a[word] = [word_cn, 0, 0]
        return True
    else:
        print("已取消录入")
        return False


def new_word_auto(a):
    print("输入英文:(输入 'exit()' 取消录入)")
    word = input()
    if word == "exit()":
        print("已取消录入")
        return False
    if word in a:
        print(word, "已经存在，请重新输入")
        word = input()
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
        browser0.close()
        for i in word_result:
            word_cn += i.text
        word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
        print(word, word_cn_complete, "确认把这个单词加入列表吗?(Y/N)")
        cfm = input()
        if cfm == "Y" or cfm == "y":
            a[word] = [word_cn_complete, 0, 0]
            return True
        else:
            print("已取消录入")
            return False
    except NoSuchWindowException:
        print("窗口异常关闭，无法继续操作。")
        return False



def show_word(a):
    for i in a:
        print(i, a[i][0])


def main(argv):
    filename = "wordlist.txt"
    a = read(filename)
    quiz_cache = deepcopy(a)
    b_shown = False
    options, args = getopt.getopt(argv, "3")
    if ('-3', '')in options or '3' in args:
        random_test(quiz_cache, a, filename)
    while True:
        show_menu()
        b = str(input())
        if b == "1":
            show_word(a)
            b_shown = True
        elif b == "2":
            if new_word(a):
                write(filename, a)
        elif b == "3":
            if b_shown:
                path = os.getcwd()
                os.system("cd "+path)
                subprocess.Popen("背单词launcher.bat -3", creationflags=subprocess.CREATE_NEW_CONSOLE)
                sys.exit()
            else:
                random_test(quiz_cache, a, filename)
        elif b == "4":
            find_word(a)
        elif b == "5":
            write(filename, a)
        elif b == "6":
            mistake_notebook = mistake_collection(a)
            for i in mistake_notebook:
                print(i[0], "做了", i[1], "次，错了", i[2], "次，错误率", round(float(i[2])/float(i[1])*100, 2), "%")
        elif b == "7":
            if new_word_auto(a):
                write(filename, a)
        elif b == "8":
            print_graph(a)
            on_progress()
        elif b == "9":
            statistics(a)
        else:
            on_progress()


if __name__ == '__main__':
    main(sys.argv[1:])
