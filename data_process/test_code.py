

#
#import numpy as np
# 测试frombuffer函数
#s = b"hello world"
#a = np.frombuffer(s, dtype='S1', count=-1, offset=0)

# print(a)

# ------------------------------------------------

# 测试字典嵌套
# 构造字典
# dict = {
#        'file1':{
#                'yorn':0,
#                'corb':1,
#                'torf':0},
#        'file2':{
#                'yorn':0,
#                'corb':1,
#                'torf':0},
#        'file3':{
#                'yorn':0,
#                'corb':1,
#                'torf':0}
#        }
# 单个值输出
# print(dict['file2']['yorn'])

# 全部值输出
# 比如要所有的yorn值
#classify = 'yorn'

#yornDict = []
# for file in dict.values():
#    print("file==>",file)
#    for key,value in file.items():
#        print("key==>",key)
#        if key=='yorn':
#            print("value===>",value)
#            yornDict.append(value)
# print("yornDict===>",yornDict)

# ------------------------------------------------
#
# 测试生成嵌套字典(1)
# 用defaultdict
#from collections import defaultdict
# 如果想生成一个嵌套的dict，如何处理，python3可以，python2貌似不可以
# file1='file1'
# file2='file2'
#ta = 1
#tb = 0
# def gen_dict():
#    return {
#        'yorn': ta,
#        'corb': tb,
#        'torf': tb,
#    }
#d_dict = defaultdict(gen_dict)
# d_dict[file1]
# d_dict[file2]
# print("d_dict==>",d_dict)


# ------------------------------------------------
##
# 测试生成嵌套字典(2)
# 用setdefault
# file1='file1'
# file2='file2'
# ta=1
# tb=0
#d = {}
#d1 = d.setdefault(file1,{})
#d2 = d1.setdefault('yorn',ta)
#d2 = d1.setdefault('corb',tb)
#d2 = d1.setdefault('torf',ta)

#d1 = d.setdefault(file2,{})
#d2 = d1.setdefault('yorn',ta)
#d2 = d1.setdefault('corb',tb)
#d2 = d1.setdefault('torf',ta)
# print(d)

# ------------------------------------------------
##
# 测试listdir
#import os

# filepath='D:/TestTrain/'
#filename = os.listdir(filepath)

# print(filename)

# ------------------------------------------------
# 问题：获取所有文件夹下的绝对路径出问题了？？？
#
# [ 'D:/FFOutput/s-6\\Sj\\sj.cfy.4.wav', 'D:/FFOutput/s-6\\Sj\\sj.ctn.1.wav'
# 使用转义符就好了
# ------------------------------------------------
# #测试 state_X and state_Y and state_N
# from check import checkFile
# #判断文件夹下是否存在文件，存在就跳过，不存在就保存
# filePath = './mid_data'
# file_X = 'X.npy'
# file_Y = 'Y.npy'
# file_N = 'N.npy'
# state_X = checkFile(filePath,file_X)
# state_Y = checkFile(filePath,file_Y)
# state_N = checkFile(filePath,file_N)
# if state_X and state_Y and state_N :
#     print(state_X and state_Y and state_N)
#     print("file exist!")
# else:
#     print("please save file!!!")

# ------------------------------------------------
# # 测试拆分数组
# import numpy as np

# data = np.random.random(size=10)
# print("data==>>", data)
# print("data.shape[0]==>>", data.shape[0])
# index_1 = np.random.choice(data.shape[0], 4, replace=False)
# print(index_1)
# data1 = data[index_1]
# print("data1==>>", data1)
# print("data1.shape[0]==>>", data1.shape[0])
# print(data1[0])
# index_2 = np.arange(data.shape[0])
# index_2 = np.delete(index_2, index_1)
# print(index_2)
# data2 = data[index_2]
# print("data2==>>", data2)
# print("data2.shape[0]==>>", data2.shape[0])
# print(data2[0])

# #
'''
==============================测试段=====================
'''
# #将所有wav文件的mfcc参数写入数组中
# mfccData.append(mfcc)

# #查看数据类型
# print(type(mfcc))
# #查看数组元素数据类型
# print(mfcc.dtype)
# #查看数据值
# print(mfcc)
# #print(wavmfcc[i])
# #查看数据的维数
# print(mfcc.shape)

# #查看数据/数据类型

# print(mfccData)
# print(type(mfccData))

#mfccData[i] = numpy.append(mfcc) #LL#
# LL#可以在这里同步计算最大长度
# max_length=max(max_length,wavmfcc[i])

# print(type(wavmfcc))
# [
# [[],[]],
# [[],[]]
# ]
'''
==============================测试段=====================
'''
# #测试加载npy文件、allow_pickle=True
# import numpy

# if __name__ == "__main__":
#     #mfcc_list = numpy.load("./mid_data/mfcc_list.npy",allow_pickle=True)
#     #mfcc_list = mfcc_list.tolist()
#     #print("======================\n",mfcc_list,"======================\n")
#     max_length = numpy.load("./mid_data/max_length.npy",allow_pickle=True)
#     max_length = max_length.tolist()
#     print(type(max_length))
#     print("max_length=====", max_length,"======================\n")
#     pass

# ------------------------------------------------
# 测试嵌套字典取数操作
# 获取所有wav文件路径
from getY import get_allFileLabel
allFilePath = 'D:/FFOutput'
dateset_rate = 0.9  # 拆分比率
trainSetLabel, testSetLabel = get_allFileLabel(allFilePath, dateset_rate)
# 字典长度
t1 = len(trainSetLabel)
t2 = len(testSetLabel)

print("len(trainSetLabel)===》", t1)
print("len(testSetLabel)===》", t2)
# 字典取值d[key]
t3 = trainSetLabel["D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"]
t4 = testSetLabel["D:/FFOUTPUT/S-1/DHY/D.1.CTN.WAV"]

print("trainSetLabel[key]===>>>", t3)
print("testSetLabel[key]===>>>", t4)
# 嵌套字典取值d[key][key]
t5 = trainSetLabel["D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"]["corb"]
t6 = trainSetLabel["D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"]["torf"]
t7 = trainSetLabel["D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"]["yorn"]

print("trainSetLabel[key][key]===>>>", t5)
print("trainSetLabel[key][key]===>>>", t6)
print("trainSetLabel[key][key]===>>>", t7)
# 通过key为变量取值
fileName = "D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"
t8 = trainSetLabel[fileName]["corb"]

print("trainSetLabel[key][key]===>>>", t8)
# 查询字典中是否有键为key的项
key = "D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"

keyState = key in trainSetLabel
print("keyState:",keyState)