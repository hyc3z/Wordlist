# iFindWord
背单词py软件

1、安装python3，并配置好环境变量

2、安装需求

<i>gui版</i>

`pip3 install pyqt5`

<i>控制台剪贴板</i>

`$ sudo apt-get install xsel xclip`

`$ sudo pip3 install pyperclip`


3、运行软件：

gui版本

    $ python3 Gui/gui.py
    
控制台剪贴板

    $ python3 Console/Clipboard.py
    
剪贴板的作用：在看文档时，遇到不会的单词，选中他，按下Ctrl+C（复制），剪贴板中会自动出现中文解释和英美音标。
目前由于未找到合适本地词库，采用了爬取在线词库方式获取信息。

---
   