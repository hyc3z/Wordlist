﻿# iFindWord
背单词py软件

1、安装python3，并配置好环境变量

2、安装需求

<i>windows</i>

`pip3 install pyperclip`

<i>linux</i>

`$ sudo apt-get install xsel xclip`
`$ sudo pip3 install pyperclip`


3、运行软件：

剪贴板Clipboard：
    
windows

    运行 clipboard.bat
    
linux

    $ python3 Clipboard_manylinux.py
    
剪贴板的作用：在看文档时，遇到不会的单词，选中他，按下Ctrl+C（复制），剪贴板中会自动出现中文解释和英美音标。
目前由于未找到合适本地词库，采用了爬取在线词库方式获取信息。

---
    
背单词iFindWord：
    
windows

    运行 背单词.bat
    
linux

    $ python3 iFindWord_linux.py
    
根据菜单选择相应功能。




<p> 初步加入Linux完整版支持

<p> Windows版本日志 </p>

    "v1.0.0": "背单词小py",
    "v1.0.1": """修复了录入单词hint的bug 修复了重新开始时只有一个单词的bug""",
    "v1.1.0": """加入了做题计数器和错误计数器，为以后更新错题集和统计图表准备，wordlist不再向下兼容，可用converter进行转换 加入了查找单词功能 加入了手动保存功能""",
    "v1.1.1": """修复了随机测试显示list而非中文的bug""",
    "v1.1.2": """修复了重新开始时闪退bug(函数漏写一个参数233)完善错题统计的后台支持""",
    "v1.2.0": """增加了错题集功能（预支持版本）现在每次做题后都能显示正确率和做题次数了""",
    "v1.3.0": "增加了智能录入功能，只需输入英文自动搜索匹配中文解释",
    "v1.3.5": """完善了爬取阶段增加图表预支持""",
    "v1.3.6": "修复了录入单词后访问错题集报错的bug",
    "v1.3.7": "从目录中移除了chromedriver，请自行下载相应版本",
    "v1.4.0": "增加统计数据功能",
    "v1.4.2": """增加了窗口异常关闭处理方法增加了搜索失败处理方法""",
    "v1.4.3": "增加了每日录入单词统计和每日做题统计",
    "v1.4.4": "修复了无法运行的bug",
    "v1.4.5": "显示图表更新到v1.0.1版本",
    "v1.4.6": "增加输入空格时的兼容性(strip())",
    "v1.4.7": "增加随机测试hint always版",
    "v1.4.8": "微调随机测试显示格式",
    "v1.4.9": "增加输入容错率",
    "v1.4.10": "调整提示的分隔显示方式，更容易分辨词组",
    "v1.4.11": "修复了每日做题统计无法显示的bug(其实是忘了写)",
    "v1.4.12": """增加KeyboardInterrupt处理方法用Decimal代替表示概率其他的一些小修改让程序更加易用""",
    "v1.5.2": "增加错题集测试功能",
    "v1.5.3": "增加自动下载chromedriver模块",
    "v1.6.0": """重构import部分，现在有进度条和管理员机制 增加管理员运行部分 增加下载文件的实时进度条 修复了自动查找chrome版的一些bug 将moduleInstaller整合进脚本内部""",
    "v1.6.1": "模糊本地查找",
    "v1.6.2": """将版本信息整合进脚本内部 使用pyc代替源代码发布release 修改了菜单结构""",
    "v1.6.3": "增加换行使版本信息更易读",
    "v1.6.4": "增加了自动录入的断线情况处理",
    "v1.6.5": "增加了词组和单词的区分",
    "v1.6.6": "现在在显示已经录入该单词时，会显示录入的单词解释",
    "v1.6.7": """保存文件换成utf-8格式 用自己写的get_path()代替了os.getcwd()，让脚本也可以开机运行时找到路径""",
    "v1.6.8": "用面向对象重构了wordlist, 累死爹了",
    "v1.7.0": "全部面向对象重构版本,beta版",
    "v1.7.1": "全部面向对象重构版本,RC版",
    "v1.7.2": "终于有了，所有单词词组的字母排序！",
    "v1.7.3": "加入直接在菜单搜索的功能",
    "v1.7.4": "修复了直接菜单搜索无法处理空格的问题, 修复了几处拼写错误",
    "v1.7.5": "增加每个单词的录入日期和按日期顺序显示",
    "v1.7.6": "修复了一些稳定性问题",
    "v1.8.0": "人工录入功能放到附加菜单，新增剪贴板",
    "v1.8.1": "用Pyperclip代替win32clipboard,相对稳定的版本,能测试带空格和'的单词和词组",
    "v1.8.2": "增强了监听剪切板的稳定性，修复了正确率显示为错误率的问题",
    "v1.8.3": """修复了睡眠恢复后监听剪切板可能报错（拒绝访问）的问题 修复了admin后窗口大小不对的问题 修复了退出后提示是否中止批处理的问题(exit()代替sys.exit()) 修复了打不开文件的问题""",
    "v1.8.4": """修复一部分稳定性问题 重新改了import 自动下载模块，更加具有可扩展性 所有单词按时间排序以及测试最近单词 简化代码，删除一些功能""",
    "v1.8.5": """修复了测试最近单词的bug 加入懒人测试模式，输入数字选择""",
    "v1.9.0": "增加保存到mysql database的功能",
    "v1.9.1": "自定义保存数据库名",
    "v1.9.2": "admin bug修复",
    "v1.9.3": "增加英译中测试",
    "v1.9.4": "修复错题集bug",
    
<p> Linux 完整版（开发中） 日志</p>

    "v0.0.1": "增加Linux支持"
    "v0.0.2": "增加复习时显示音标功能 修复一些bug"
    
<p> Clipboard For Linux 日志</p>
    
    增加超时重连
    增加英美音标爬取
    
