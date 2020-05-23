import tensorflow as tf
import numpy as np
import json 
#引入get_RNN_x

def corb(wavpath,dct,weights,biases):
    x=get_RNN_x(wavpath=wavpath,dct=dct)
    result = tf.matmul(x,weights) + biases
    #取RNN的最后一个输出作为返回值  
    ##根据result的类型来处理：
    ##百分值的话，判断偏C还是偏B；
    ##0/1的话直接返回；
    return result

if __name__=='__main__':
    #添加新的音频文件路径
    wavpath='' 
    #训练后得到的 权重
    weights=np.load("./paramters/weights")  
    #训练后得到的 偏置
    biases=np.load("./paramters/biases")               
    #得到分类结果  C or B ?
    print(corb(wavpath=wavpath,dct=13,weights=weights,biases=biases))
    pass