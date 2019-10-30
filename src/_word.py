import datetime
from decimal import Decimal
class Word:

    def __init__(self, enword, cnexplanation, testedcount=0, correctcount=0, searchtime=0, recordedtime=str(datetime.datetime.now())):
        self.__enWord = enword
        self.__cnExplanation = cnexplanation
        self.__testedCount = testedcount
        self.__correctCount = correctcount
        self.__searchTime = searchtime
        self.__Visited = False
        self.__recordedTime = recordedtime
        self.__recordedDate = recordedtime[0:10]

    def it_self(self, mysql_format=False):
        if not mysql_format:
            return self.__enWord
        else:
            return str(repr(self.__enWord))

    def explanation(self, mysql_format=False):
        if not mysql_format:
            return self.__cnExplanation
        else:
            return str(repr(self.__cnExplanation))

    def tested_count(self, mysql_format=False):
        if not mysql_format:
            return self.__testedCount
        else:
            return str(repr(str(self.__testedCount)))

    def correct_count(self, mysql_format=False):
        if not mysql_format:
            return self.__correctCount
        else:
            return str(repr(str(self.__correctCount)))

    def recorded_date(self, mysql_format=False):
        if not mysql_format:
            return self.__recordedDate
        else:
            return str(repr(self.__recordedDate))

    def recorded_time(self, mysql_format=False):
        if not mysql_format:
            return self.__recordedTime
        else:
            return str(repr(self.__recordedTime))

    def incorrect_count(self, mysql_format=False):
        if not mysql_format:
            return self.__testedCount-self.__correctCount
        else:
            return str(repr(str(self.__testedCount-self.__correctCount)))

    def searched_count(self, mysql_format=False):
        if not mysql_format:
            return self.__searchTime
        else:
            return str(repr(str(self.__searchTime)))

    def visited(self, mysql_format=False):
        if not mysql_format:
            return self.__Visited
        else:
            return str(repr(int(self.__Visited)))

    def correct_rate(self):
        return round(Decimal(self.__correctCount/self.__testedCount * 100.0), 2)

    def incorrect_rate(self):
        return round(Decimal((self.__testedCount-self.__correctCount) / self.__testedCount* 100.0), 2)

    def numeric_data(self):
        return str(self.__testedCount)+" "+str(self.__correctCount)+" "+str(self.__searchTime)

    def correct(self):
        self.__testedCount += 1
        self.__correctCount += 1

    def incorrect(self):
        self.__testedCount += 1

    def searched(self):
        self.__searchTime += 1

    def show_rate(self):
        print(self.it_self(), "已做", self.tested_count(), "次，正确", self.correct_count(), "次，正确率", self.correct_rate(), "%")#在1.8.2版本修复

    def visit(self):
        self.__Visited = True

    def unvisit(self):
        self.__Visited = False

    def change_explanation(self, new_explanation):
        self.__cnExplanation = new_explanation

    def is_phrase(self):
        k = self.__enWord.split(' ')
        return len(k)>1

