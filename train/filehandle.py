import re


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

def fileSplit(sourcefile,trainfile,testfile,rate):
    with open(sourcefile,'r',encoding='utf-8') as source:
        contents = source.readlines()
        count = int(len(contents)*rate)
        train = contents[0:count]
        test = contents[count:-1]
        with open(trainfile,'w',encoding='utf-8') as file1:
            file1.writelines(train)
        with open(testfile, 'w', encoding='utf-8') as file2:
            file2.writelines(test)


def file2vector(inputFile):
    with open(inputFile,'r',encoding='utf-8') as infile:
        contents = infile.readlines()
        words = {}
        i=0
        for line in contents:
            # line=re.sub('([0-9０-９]+)','1',line)
            result = line.split(' ')
            for i,e in enumerate(result):
                if e:
                    if e not in words.keys():
                        words[e] = [0,i]
                    else:
                        words[e][0] += 1
    return words
def deletespace(inputFile,outputFile):
    with open(inputFile,'r',encoding='utf-8') as infile:
        outfile =  open(outputFile,'w',encoding='utf-8')
        contents = infile.readlines()
        for line in contents:
            line = line.replace(' ','')
            if line.strip():
                outfile.write(line)
        outfile.close()


if __name__ == '__main__':
    deletespace("train_1.txt","train_final.txt")



