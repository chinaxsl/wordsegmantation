import re


#文件去除数字和字母
def handleFile(inputFile,outputFile):
    with open(inputFile, 'r', encoding='utf-8') as infile:
        outfile = open(outputFile,'w',encoding='utf-8')
        contents = infile.readlines()
        result = []
        for line in contents:
            line = re.sub(u'([0-9]+-[0-9]+-[0-9]+-[0-9]+)','',line)
            line = re.sub(u'(/[a-zA-Z]+)|\[|(\][a-zA-z]*)' ,'',line)
            line = re.sub(u'  ',' ',line)
            result.append(line)
        outfile.writelines(result)
        outfile.close()
#将语料文件分为训练集和测试集 训练集：测试集 = rate：1
def fileSplit(sourcefile,trainfile,testfile,rate):
    with open(sourcefile,'r',encoding='utf-8') as source:
        contents = source.readlines()
        count = int(len(contents)*rate)
        train = contents[0:count]
        train = [line.lstrip() for line in train]
        test = contents[count:-1]
        test = [line.lstrip() for line in test]
        with open(trainfile,'w',encoding='utf-8') as file1:
            file1.writelines(train)
        with open(testfile, 'w', encoding='utf-8') as file2:
            file2.writelines(test)

# #中文转换为词向量
# def file2vector(inputFile):
#     with open(inputFile,'r',encoding='utf-8') as infile:
#         contents = infile.readlines()
#         words = {}
#         i=0
#         for line in contents:
#             # line=re.sub('([0-9０-９]+)','1',line)
#             result = line.split(' ')
#             for i,e in enumerate(result):
#                 if e:
#                     if e not in words.keys():
#                         words[e] = [0,i]
#                     else:
#                         words[e][0] += 1
#     return words
#消除文件内容中的空格
def deletespace(inputFile,outputFile):
    with open(inputFile,'r',encoding='utf-8') as infile:
        outfile =  open(outputFile,'w',encoding='utf-8')
        contents = infile.readlines()
        for line in contents:
            line = line.replace(' ','')
            if line.strip():
                outfile.write(line)
        outfile.close()
#消除文件句首空格
def filelstrip(inputFile,outputFile):
    with open(inputFile,'r',encoding='utf-8') as infile:
        contents = infile.readlines()
        contents = [line.lstrip() for line in contents]
        outFile = open(outputFile,'w',encoding='utf-8')
        outFile.writelines(contents)

if __name__ == '__main__':
    # deletespace("train_1.txt","train_final.txt")
    # filelstrip("train_1.txt","train_2.txt")
    fileSplit('source.txt','train.txt','test.txt',0.7)



