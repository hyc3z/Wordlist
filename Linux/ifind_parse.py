import re
import requests
from requests.exceptions import RequestException
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

