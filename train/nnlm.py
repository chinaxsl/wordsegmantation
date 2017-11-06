from train.filehandle import file2vector
import numpy as np

class classifier:
    file = 'train_1.txt'
    def inputLayer(self,n=50):
        #加载中文词典
        word_dict = file2vector(self.file)
        #获得字典长度L
        word_dict_length = len(word_dict)
        #初始化映射矩阵C   C的维数为L*n
        np.random.seed(1)
        C = np.random.randn(word_dict_length,n)

