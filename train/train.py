import copy
import re
import time
from utils.filehandle import writeResult
from utils.graph import create
from decimal import *


#两种方法实现基于BiGram的最大概率中文切分
#1 根据词典列出所有可能的切分组合，根据Bigram计算各种切分的概率，取最大概率的切分为最后结果
#2 将句子切分成长度小于maxLen的若干个词语 使用词语作为边 切分点作为节点 建立DAG  对DAG进行DP计算最大概率，再回溯得到最大概率的切分结果
class ModelTrain:
    #初始化中文词典和左邻词频次
    def __init__(self):
        file = open('source.txt','r',encoding='utf-8')
        contents = file.readlines()
        self.words,self.words_length = self.createDict(contents)
        self.words_LAW = self.findLAW(contents)


    #根据语料库生成中文词典
    def createDict(self,contents):
        words = {}
        words_length = 0
        for line in contents:
            result = line.split()
            for e in result:
                if e:
                    words_length += 1
                    if e not in words.keys():
                        words[e] = 1
                    else:
                        words[e] += 1
        words_length += len(words)
        return words,words_length

    #根据预料库查找每个词的左邻词并记录每个左邻词出现的频次
    def findLAW(self,contents):
        word_LAW = {}
        for line in contents:
            result =line.split()
            length =len(result)
            for index in range(length):
                #判断不是句首词，则必定有左邻词
                if index:
                    #这个词有过左邻词
                    if result[index] in word_LAW.keys():
                        #该左邻词之前出现过
                        if result[index-1] in word_LAW[result[index]]:
                            word_LAW[result[index]][result[index-1]] += 1
                        else:
                            word_LAW[result[index]][result[index-1]] = 1

                    else:
                        word_LAW[result[index]] = {result[index-1]:1}
                else:
                    if result[index] not in word_LAW.keys():
                        word_LAW[result[index]] = {}
        return word_LAW

    #递归切分语句 根据词典列出所有可能的切分组合
    def cut(self, text, start, maxLen,cut_group=[]):
        length = len(text)
        if start==length:
            self.cut_groups.append(copy.deepcopy(cut_group))
        else:
            for index in reversed(range(2,maxLen+1)):
                if start+index<=length and text[start:start+index] in self.words:
                    cut_group.append(text[start:start + index])
                    self.cut(text, start + index, maxLen,cut_group)
                    cut_group.pop()
            if text[start] in self.words:
                cut_group.append(text[start:start + 1])
                self.cut(text, start + 1, maxLen, cut_group)
                cut_group.pop()

    #把句子切分成若干个长度小于maxLen的词语
    def _cut(self,text,maxLen):
        length = len(text)
        cut_words = []
        for start in range(length):
            for index in range(1,maxLen):
                if start+index > length:
                    break
                cut_word = text[start:start+index]
                if cut_word in self.words or len(cut_word) == 1:
                    node = {}
                    node['text'] = cut_word
                    node['start'] = start
                    node['end'] = start+index
                    cut_words.append(node)
        graph = create(cut_words,text)
        return self.Dp(graph,text)

    #计算word的左邻词总数
    def countLawtimes(self,word):
        count = 0
        for key in self.words_LAW[word].keys():
            count += self.words_LAW[word][key]
        # count += len(self.words_LAW[word])
        return count

    #对DAG进行DP计算最大概率，最后回溯得到切分结果
    def Dp(self,graph,text):
        sentence_begin = graph[0]['edge_head']
        graph[0]['probility'] = Decimal(1)
        for edge in sentence_begin:
            if edge['text'] in self.words:
                probility = Decimal.from_float(self.words[edge['text']]/self.words_length)
            else:
                probility = Decimal.from_float(1/self.words_length)
            graph[edge['end']]['probility'] = graph[0]['probility'] * probility
            graph[edge['end']]['best_law'] = 0
        for index in range(1,len(text)+1):
            edges = graph[index]['edge_head']
            for edge in edges:
                begin = edge['start']
                end = edge['end']
                if edge['text'] in self.words:
                    previous_edges = graph[begin]['edge_tail']
                    for previous_edge in previous_edges:
                        if edge['text'] in self.words_LAW.keys()and previous_edge['text'] in self.words_LAW[edge['text']]:
                            law_count = self.countLawtimes(edge['text'])
                            condition_p = graph[begin]['probility'] * self.words_LAW[edge['text']]\
                                                              [previous_edge['text']]/law_count
                        else:
                            condition_p = graph[begin]['probility'] / self.words_length
                        if condition_p > graph[end]['probility']:
                            graph[end]['probility'] = condition_p
                            graph[end]['best_law'] = begin

                else:
                    condition_p = graph[begin]['probility'] / self.words_length
                    if condition_p > graph[end]['probility']:
                        graph[end]['probility'] = condition_p
                        graph[end]['best_law'] = begin
        start = len(text)
        result = []
        while(start):
            word = text[graph[start]['best_law']:start]
            result.append(word)
            start = graph[start]['best_law']
        final_result = list(reversed(result))
        return " ".join(final_result)


    #从所有的切分组合中找到概率最大的切分
    def getMaxProGroup(self,cut_groups):
        MaxProbility = Decimal(0)
        Max = []
        for cut_group in cut_groups:
            Probility = self.getProbility(cut_group)
            if Probility > MaxProbility:
                Max = cut_group
                MaxProbility = Probility
        return Max

    #根据Bigram语言模型计算中文词概率  采用加1平滑
    #1、句首词 P = 词典出现频次+1/ 语料文件的词总数 + 词典的词总数
    #2、非句首词 P = 出现该左邻词频次+1 / 左邻词总数+不同左邻词数
    #3、OOV词 P = 1/ 语料文件的词总数 + 词典的词总数
    def getProbility(self,cut_group):
        probility = Decimal(1)
        length = len(cut_group)
        for index in range(length):
            if index and cut_group[index] in self.words:
                    probility *= Decimal(self.words[cut_group[index]])/self.words_length
            elif cut_group[index] in self.words:
                law_count = self.countLawtimes(cut_group[index])
                if cut_group[index-1] in self.words_LAW[cut_group[index]]:
                    probility *= Decimal(self.words_LAW[cut_group[index]][cut_group[index-1]])/law_count
                else:
                    probility *= Decimal(1)/self.words_length
            else:
                probility *= Decimal(1)/self.words_length
        return probility



    #从文件内容中读取待切分的内容,内容分为若干行
    #每行内容又按标点切分成多段，最后按段切分以减少切分句子的长度，提高切分速度
    def getCutResult(self,contents_before):
        self.cut_groups = []
        contents_after =[]
        count = 0
        begin = time.time()
        for line in contents_before:
            count+=1
            print(count)
            result = re.split('(：|-|/|【|？|】|\?|。|，|\.|、|《|》| |（|）|”|“|；|\n)', line)
            sentence = []
            for word in result:
                if word:
                    self.cut_groups.clear()
                    self.cut(word,0,6)
                    temp = self.getMaxProGroup(self.cut_groups)
                    sentence += temp
            content = " ".join(sentence)+'\n'
            contents_after.append(content)
        end = time.time()
        print(end-begin)
        return "".join(contents_after)


    #优化后的DAG切分实现
    def _getCutResult(self,contents_before):
        contents_after = []
        count = 0
        begin = time.time()
        for line in contents_before:
            count+=1
            print(count)
            content = self._cut(line,6)
            contents_after.append(content)
        end = time.time()
        print(end - begin)
        return "".join(contents_after)


model = ModelTrain()
file = open('train_final.txt','r',encoding='utf-8')
line = file.readlines()
contents_after = model._getCutResult(line)
writeResult('2017111457.txt',contents_after)