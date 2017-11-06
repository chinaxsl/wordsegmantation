from train.filehandle import file2vector

def main():
    #加载中文词典
    word_dict = file2vector("train_1.txt")
    #获得字典长度L
    word_dict_length = len(word_dict)