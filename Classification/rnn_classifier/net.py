from __future__ import print_function

import tensorflow as tf
import random
import numpy as np

# 运行的参数
class Net_Parameters:
    ##从get函数里面得到mfcc的输出
    #dct窗口数
    dct=13
    #格式化后的数据，numpy arr形式
    batch_data =None
    #数据标签
    batch_labels=None
    #mfcc vector的实际（计算）长度
    batch_seqlen=None 
    ##网络优化的学习率  ,默认0.01
    learning_rate = 0.01
    ##网络训练轮数，默认1,000,000
    training_iters = 1000000
    ##数据量多少
    batch_size = batch_data.shape[0]            
    ##以特定步长来显示中间输出
    display_step = 10 
    ##定义数据集分离比率
    dataset_rate=0.9
    # 网络定义时的参数
    ##最大的序列长度，需要根据所有的mfcc vector来计算最大长度
    seq_max_len = batch_data.shape[2]
    ## 隐层的size，我们考虑的时候128或者256
    n_hidden = 64 
    ## 类别数，这里我们是单分类器
    n_classes = 2 
    ##训练数据集 数据量90%
    #随机返回90%的数据，然后从原来的数组中删除
    ##测试数据集 数据量10%
    ##把剩下的数组中的值赋给测试集
    train_set,test_set=dividide

    # x为输入，y为输出
    # None的位置实际为batch_size
    x = tf.placeholder("float", [None, seq_max_len],dct=dct)
    y = tf.placeholder("int", [None, n_classes])
    # 这个placeholder存储了输入的x中，每个mfcc vector的实际长度
    seqlen = tf.placeholder(tf.int32, [None])

    # weights和bias其实就是模型的参数，也是计算得到的核心
    weights = {
        'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
    }
    biases = {
        'out': tf.Variable(tf.random_normal([n_classes]))
    }
    pass