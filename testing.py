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

word = "rip"
word_cn = ""
browser0 = webdriver.Chrome()
wait = WebDriverWait(browser0, 5)
browser0.get("http://dict.youdao.com/w/eng/"+word+"/#keyfrom=dict2.index")
try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'trans-container')))
    word_result = browser0.find_elements_by_css_selector('#phrsListTab > div.trans-container > ul > li')
    for i in word_result:
        word_cn += i.text
    word_cn_complete_youdao = word_cn.replace('\n', "").replace('\r', "")
    print(word_cn_complete_youdao)
except TimeoutException:
    pass