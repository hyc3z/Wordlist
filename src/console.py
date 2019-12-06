import re
import random
import os
import sys
import getopt
from random import choice
from datetime import date
from _wordlist import WordList
from ifind_parse import get_one_page,parse_one_page,get_phonetic,impatient_search
from clipboard_version import get_version

date_today = str(date.today())
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
