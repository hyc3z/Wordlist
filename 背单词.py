try:
    import re
    from random import choice
    import random
    import sys
    import os
    import getopt
    import subprocess
    import requests
    from requests.exceptions import RequestException
    import zipfile
    from datetime import date
    from copy import deepcopy
    import time
    print("loading ... 25%")
    import matplotlib.pyplot as plt
    print("loading ... 50%")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    print("loading ... 75%")
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchWindowException
    from selenium.common.exceptions import WebDriverException
    from decimal import Decimal
    print("loading ... 100%")
except ModuleNotFoundError:
    print("模组安装不完全，是否自动下载安装？(y/n)")
    chx = input().strip().lower()
    while len(chx) == 0:
        chx = input().strip().lower()
    if chx == 'y':
        subprocess.Popen("moduleInstaller.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()
    else:
        sys.exit()
except KeyboardInterrupt:
    print("用户中断执行...")
    sys.exit()

minimum_requirement = 29
maximum_support = 70
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
    "70": "2.42"
}


def read(filename):
    try:
        f = open(filename, "r")
        strn = f.read()
        fpt = {}
        res = re.split('\n', strn)
        for i in range(1, len(res), 4):
            fpt[res[i-1]] = [res[i], int(res[i+1]), int(res[i+2]), int(res[i+1])-int(res[i+2])]
        f.close()
    except FileNotFoundError:
        f = open(filename, "w+")
        fpt = {}
        f.close()
    return fpt


def read_date(filename):
    try:
        f = open(filename, "r")
        strn = f.read()
        fpt = {}
        res = re.split('\n', strn)
        for i in range(1, len(res), 3):
            fpt[res[i - 1]] = [int(res[i]), int(res[i+1])]
        f.close()
    except FileNotFoundError:
        f = open(filename, "w+")
        fpt = {}
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
    print("背单词v1.5.3")
    print("1:显示所有单词")
    print("2:录入新单词")
    print("3:随机测试")
    print("4:随机测试hint always版")
    print("5:查找单词")
    print("6:手动保存")
    print("7:错题集")
    print("8:自动录入chrome版")
    print("9:自动录入requests版")
    print("0:显示图表")
    print("X:统计数据")
    print("R:把所有单词替换成有道词典版本")


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


def mistake_collection(wordlist, b, cur_date, filename, datefile):
    soup = []
    testsoup = {}
    for i in wordlist:
        if (wordlist[i][1]-wordlist[i][2]) > 0:
            soup.append([i, wordlist[i][1], wordlist[i][1]-wordlist[i][2]])
    soup.sort(key=lambda x: Decimal(float(x[2]))/Decimal(float(x[1])), reverse=True)
    for i in soup:
        print(i[0], "做了", i[1], "次，错了", i[2], "次，错误率", round(float(i[2]) / float(i[1]) * 100, 2), "%")
        testsoup[i[0]] = wordlist[i[0]]
    print("准备好进行错题测试吗？（y/n)")
    chx = input().strip().lower()
    while len(chx) == 0:
        chx = input().strip().lower()
    if chx == 'y':
        random_test_hint_always(testsoup, wordlist, filename, b, cur_date, datefile)
    return soup


def find_word(wordlist):
    print("输入查找的单词：")
    a = input().strip().lower()
    while len(a) == 0:
        a = input().strip().lower()
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
    ans = input().strip().lower()
    while len(ans) == 0:
        ans = input().strip().lower()
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
        ans = input().strip().lower()
        while len(ans) == 0:
            ans = input().strip().lower()
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
                chx = input().strip().lower()
                while len(chx) == 0:
                    chx = input().strip().lower()
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
                chx = input().strip().lower()
                while len(chx) == 0:
                    chx = input().strip().lower()
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
                chs = input().strip().lower()
                while len(chs) == 0:
                    chs = input().strip().lower()
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
        chs = input().strip().lower()
        while len(chs) == 0:
            chs = input().strip().lower()
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
    ans = input().strip().lower()
    while len(ans) == 0:
        ans = input().strip().lower()
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
            chx = input().strip().lower()
            while len(chx) == 0:
                chx = input().strip().lower()
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
        chs = input().strip().lower()
        while len(chs) == 0:
            chs = input().strip().lower()
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
    word = input().strip().lower()
    while len(word) == 0:
        word = input().strip().lower()
    if word == "exit()":
        print("已取消录入")
        return False
    if word in a:
        print(word, "已经存在，请重新输入")
        word = input().strip().lower()
        while len(word) == 0:
            word = input().strip().lower()
        if word == "exit()":
            print("已取消录入")
            return False
    print("输入中文：(输入 'exit()' 取消录入)")
    word_cn = input().strip().lower()
    while len(word_cn) == 0:
        word_cn = input().strip().lower()
    if word_cn == "exit()":
        print("已取消录入")
        return False
    print(word, word_cn, "确认把这个单词加入列表吗?(Y/N)")
    cfm = input().strip().lower()
    while len(cfm) == 0:
        cfm = input().strip().lower()
    if cfm == "Y" or cfm == "y":
        a[word] = [word_cn, 0, 0]
        b[cur_date][0] += 1
        return True
    else:
        print("已取消录入")
        return False


def new_word_auto_chrome(a, cur_date, b):
    try:
        word_cn = ""
        word_cn_complete_youdao = ""
        word_cn_complete_baidu = ""
        word_cn_complete_baidufanyi = ""
        print("输入英文:(输入 'exit()' 取消录入)")
        word = input().strip().lower()
        while len(word) == 0:
            word = input().strip().lower()
        if word == "exit()":
            print("已取消录入")
            return False
        if word in a:
            print(word, "已经存在，请重新输入")
            word = input().strip().lower()
            while len(word) == 0:
                word = input().strip().lower()
            if word == "exit()":
                print("已取消录入")
                return False
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
                    print(download_url)
                    print("下载中...")
                    r = requests.get(download_url)
                    with open("chromedriver.zip", "wb") as code:
                        code.write(r.content)
                    z = zipfile.ZipFile('chromedriver.zip', 'r')
                    print("解压中...")
                    z.extractall(path=os.getcwd())
                    z.close()
                    print("安装完成！")
                    subprocess.Popen("背单词launcher.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
                    sys.exit()
                except KeyError:
                    if int(ver_num) < 29:
                        print("很抱歉，您的chrome版本低于", minimum_requirement, "，无法使用该功能")
                    elif int(ver_num) > 70:
                        print("很抱歉，您的chrome版本高于", maximum_support, "，无法使用该功能")
            else:
                return False
        wait = WebDriverWait(browser0, 5)
        browser0.get("https://www.baidu.com/")
        browser0.find_element_by_id("kw").send_keys(word)
        browser0.find_element_by_id("su").click()
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pc')))
            word_result = browser0.find_elements_by_class_name("op_dict3_english_result_table")
            if len(word_result) is not 0:
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
                    return False
        if len(word_cn_complete_baidu) is not 0:
            print("1、百度搜索：", word_cn_complete_baidu)
        else:
            print("百度搜索未找到匹配结果。")
        if len(word_cn_complete_baidufanyi) is not 0:
            print("2、百度翻译：", word_cn_complete_baidufanyi)
        else:
            print("百度翻译未找到匹配结果。")
        if len(word_cn_complete_youdao) is not 0:
            print("3、有道词典：", word_cn_complete_youdao)
        else:
            print("有道词典未找到匹配结果。")
        print("选择要录入的结果序号：")
        cfm = input().strip().lower()
        while len(cfm) == 0:
            cfm = input().strip().lower()
        if cfm == "1":
            if len(word_cn_complete_baidu) is not 0:
                a[word] = [word_cn_complete_baidu, 0, 0]
                b[cur_date][0] += 1
                return True
            else :
                print("已取消录入")
                return False
        elif cfm == "2":
            if len(word_cn_complete_baidufanyi) is not 0:
                a[word] = [word_cn_complete_baidufanyi, 0, 0]
                b[cur_date][0] += 1
                return True
            else :
                print("已取消录入")
                return False
        elif cfm == "3":
            if len(word_cn_complete_youdao) is not 0:
                a[word] = [word_cn_complete_youdao, 0, 0]
                b[cur_date][0] += 1
                return True
            else :
                print("已取消录入")
                return False
        else:
            print("已取消录入")
            return False
    except NoSuchWindowException:
        print("窗口异常关闭，无法继续操作。")
    except WebDriverException:
        print("引擎异常，无法继续操作。")



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
        return None


def new_word_auto_requests(a, cur_date, b):
    print("输入英文:(输入 'exit()' 取消录入)")
    word = input().strip().lower()
    word_cn = ""
    while len(word) == 0:
        word = input().strip().lower()
    if word == "exit()":
        print("已取消录入")
        return False
    if word in a:
        print(word, "已经存在，请重新输入")
        word = input().strip().lower()
        while len(word) == 0:
            word = input().strip().lower()
        if word == "exit()":
            print("已取消录入")
            return False
    page_src = get_one_page("http://dict.youdao.com/w/eng/"+word+"/#keyfrom=dict2.index")
    try:
        items = parse_one_page(page_src)
        for i in items:
            word_cn += i
        word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
        print(word, word_cn_complete, "确认把这个单词加入列表吗?(Y/N)")
        cfm = input().strip().lower()
        while len(cfm) == 0:
            cfm = input().strip().lower()
        if cfm == "Y" or cfm == "y":
            a[word] = [word_cn_complete, 0, 0]
            b[cur_date][0] += 1
            return True
        else:
            print("已取消录入")
            return False
    except AttributeError:
        print("有道词典未找到", word, "！")


def replace_youdao(a):
    k = deepcopy(a)
    count = 0
    total = len(k)
    for word in a:
        word_cn = ""
        page_src = get_one_page("http://dict.youdao.com/w/eng/" + word + "/#keyfrom=dict2.index")
        try:
            items = parse_one_page(page_src)
            for i in items:
                word_cn += i
            word_cn_complete = word_cn.replace('\n', "").replace('\r', "")
            k[word][0] = word_cn_complete
            count += 1
            print(word, word_cn_complete, "替换成功", count, "/", total)
        except AttributeError:
            count += 1
            print("有道词典未找到", word, "！")
            continue
    return k


def show_word(a):
    for i in a:
        print(i, a[i][0])


def main(argv):
    filename = "wordlist.txt"
    a = read(filename)
    datefile = "datefile.txt"
    b = read_date(datefile)
    # cur_date = str(time.strftime('%Y-%m-%d', time.localtime()))
    cur_date = str(date.today())
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
        c = input().strip().lower()
        while len(c) == 0:
            c = input().strip().lower()
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
            mistake_collection(a, b, cur_date, filename, datefile)
        elif c == "8":
            if new_word_auto_chrome(a, cur_date, b):
                write(filename, a)
                write_date(datefile, b)
                print("今天共录入了", b[cur_date][0], "个单词，加油！")
        elif c == "9":
            if new_word_auto_requests(a, cur_date, b):
                write(filename, a)
                write_date(datefile, b)
                print("今天共录入了", b[cur_date][0], "个单词，加油！")
        elif c == "0":
            print_graph(b)
            on_progress()
        elif c == "x":
            statistics(a, cur_date, b)
        elif c == "r":
            a = replace_youdao(a)
            write(filename, a)
        else:
            on_progress()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("用户中断执行...")
