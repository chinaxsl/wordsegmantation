import copy
import re

class ModelTrain:
    #初始化中文词典和左邻词频次
    def __init__(self):
        file = open('train_1.txt','r',encoding='utf-8')
        contents = file.readlines()
        self.words,self.words_length = self.createDict(contents)
        self.words_LAW = self.findLAW(contents)
        self.count=0


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
        return word_LAW
    #递归切分语句 根据词典列出所有可能的切分组合
    def cut(self, text, start, maxLen,cut_group=[]):
        length = len(text)
        if start==length:
            self.cut_groups.append(copy.deepcopy(cut_group))
        else:
            for interval in reversed(range(1,maxLen+1)):
                if start+interval<=length and text[start:start+interval] in self.words:
                    cut_group.append(text[start:start + interval])
                    self.cut(text, start + interval, maxLen,cut_group)
                    cut_group.pop()

    #从所有的切分组合中找到概率最大的切分
    def getMaxProGroup(self,cut_groups):
        MaxProbility = 0
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
        probility = 1.0
        length = len(cut_group)
        for index in range(length):
            if index and cut_group[index] in self.words:
                    probility *= self.words[cut_group[index]]+1/self.words_length
            elif cut_group[index] in self.words:
                law_count = 0
                for key in self.words_LAW[cut_group[index]].keys():
                    law_count += self.words_LAW[cut_group[index]][key]+1
                if cut_group[index-1] in self.words_LAW[cut_group[index]]:
                    probility *= self.words_LAW[cut_group[index]][cut_group[index-1]]+1/law_count
                else:
                    probility *= 1/law_count
            else:
                probility *= 1/self.words_length
        return probility


    #将分词后的结果输出到文件
    def writeResult(self,outputFile,contents_after):
        with open(outputFile,'w',encoding='utf-8') as outfile:
            outfile.writelines(contents_after)

    #从文件内容中读取待切分的内容,内容分为若干行
    #每行内容又按标点切分成多段，最后按段切分以减少切分句子的长度，提高切分速度
    def getCutResult(self,contents_before):
        self.cut_groups = []
        contents_after =[]
        length = len(contents_before)
        contents_before = contents_before[0:10]
        count = 0
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
            content = " ".join(sentence)+"\n"
            contents_after.append(content)
        return "".join(contents_after)

model = ModelTrain()
# text = "１２月３１日，中共中央总书记、国家主席江泽民发表１９９８年新年讲话《迈向充满希望的新世纪》。（新华社记者兰红光摄）"
file = open('train_final.txt','r',encoding='utf-8')
line = file.readlines()
contents_after = model.getCutResult(line)
# print(contents_after)
model.writeResult('2017111457.txt',contents_after)