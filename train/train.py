import copy
import time
import re

class ModelTrain:
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

    def cut(self, text, start, maxLen,cut_group=[]):
        length = len(text)
        if start==length:
            self.cut_groups.append(copy.deepcopy(cut_group))
        else:
            flag = False
            for interval in reversed(range(1,maxLen+1)):
                if start+interval<=length and text[start:start+interval] in self.words:
                    flag = True
                    cut_group.append(text[start:start + interval])
                    self.cut(text, start + interval, maxLen,cut_group)
                    cut_group.pop()

                # print(self.count)
                # print(cut_result)



    def getMaxProGroup(self,cut_groups):
        MaxProbility = 0
        Max = None
        for cut_group in cut_groups:
            Probility = self.getProbility(cut_group)
            if Probility > MaxProbility:
                Max = cut_group
                MaxProbility = Probility
        return Max

    def getProbility(self,cut_group):
        probility = 1.0
        length = len(cut_group)
        for index in range(length):
            if index and cut_group[index] in self.words:
                    probility *= self.words[cut_group[index]]/self.words_length
            elif cut_group[index] in self.words:
                law_count = 0
                for key in self.words_LAW[cut_group[index]].keys():
                    law_count += self.words_LAW[cut_group[index]][key]+1
                if cut_group[index] in self.words_LAW[cut_group[index]]:
                    probility *= self.words_LAW[cut_group[index]][cut_group[index-1]]+1/law_count
                else:
                    probility *= 1/law_count
            else:
                probility *= 1/self.words_length
        return probility

    def writeResult(self,outputFile,contents_after):
        with open(outputFile,'w',encoding='utf-8'):
            outputFile.writelines(contents_after)

    def getCutResult(self,contents_before):
        self.cut_groups = []
        contents_after =[]
        length = len(contents_before)
        # contents_before = contents_before[0:10]
        result = re.split('：|-|/|【|？|】|\?|。|，|\.|、|《|》| |（|）|”|“|；|\n',text)
        str_c = ''
        for i in result:
            self.cut_groups.clear()
            self.cut(i,0,6)
            i = self.getMaxProGroup(self.cut_groups)
            contents_after += i
        return contents_after


    # def test(self):
    #     text = '１２月３１日，中共中央总书记、国家主席江泽民发表１９９８年新年讲话《迈向充满希望的新世纪》。（新华社记者兰红光摄）'
    #     cut_groups=[]
    #     begin = time.time()
    #     self.cut_groups = []
    #     self.cut(text,0,6)
    #     print("划分完成")
    #     result = self.getMaxProGroup(self.cut_groups)
    #     end = time.time()
    #     print(result)
    #     print(end-begin)
    #     return result

model = ModelTrain()
text = "１２月３１日，中共中央总书记、国家主席江泽民发表１９９８年新年讲话《迈向充满希望的新世纪》。（新华社记者兰红光摄）"
# file = open('train_final.txt','r',encoding='utf-8')
# text = file.readlines()
contents_after = model.getCutResult(text)
print(contents_after)
# model.writeResult('2017111457.txt',contents_after)
# print(model.test())