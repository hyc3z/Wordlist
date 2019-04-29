import os
import re
import pyperclip
import signal
from requests import RequestException
import time
from datetime import date
import string
import sys
from _wordlist import WordList
from ifind_parse import get_one_page,parse_one_page,get_phonetic,impatient_search
from clipboard_version import get_version
import signal

def shutdownFunction0(signalnum, frame):
    os.system('rm -f '+os.path.join(sys.path[0], '~clipboard.lock'))
    exit()
    return

def shutdownFunction1(signalnum, frame):
    exit()
    return


date_today = str(date.today())

def monitor_clipboard(wordlist):
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
                clip_data = clip_data.replace('-\r', '')
                clip_data = clip_data.replace('- ', '')
                # print(clip_data)
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
    monitor_clipboard(wordlist)


if __name__ == '__main__':
    try:
        try:
            for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
                signal.signal(sig, shutdownFunction1)

            while os.path.exists(os.path.join(sys.path[0], '~clipboard.lock')):
                time.sleep(1)
                print('Unable to unlock ', os.path.join(sys.path[0], '~clipboard.lock'),'with PID=')
                os.system('cat '+os.path.join(sys.path[0], '~clipboard.lock'))
        except:
            exit()
        for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
            signal.signal(sig, shutdownFunction0)
        print(get_version())
        os.system('echo '+str(os.getpid())+' > '+os.path.join(sys.path[0], '~clipboard.lock'))
        main()
    except KeyboardInterrupt:
        os.system('rm -f '+os.path.join(sys.path[0], '~clipboard.lock'))
        exit()