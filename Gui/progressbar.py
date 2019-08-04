class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0,
                 ):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.sep = sep
        self.percentage = count/total*100
        self.percentmark = '%'

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count / self.chunk_size, self.unit, self.sep, self.total / self.chunk_size, self.unit, self.percentage, self.percentmark)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status != None:
        self.percentage = self.count/self.total*100
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)