# coding: utf-8
import librosa
import numpy
import pandas
import json
import os
from getY import get_y
from getY import get_mark
from getY import get_allFileLabel
from check import checkFile
from divideDataset import divide_dataset

# 使用librosa库将划分训练集绝对路径下的语音数据进行提取MFCC参数

def get_mfcc_list(allFilePath, n_mfcc, dateset_rate):
    # 使用划分后的训练集获取语音参数
    trainSetFile, _ = divide_dataset(allFilePath, dateset_rate)
    print(type(trainSetFile))  # <class 'numpy.ndarray'>
    #trainSetFile = trainSetFile.tolist()
    print(type(trainSetFile))
    wavmfcc = {}
    mfcc_list = []  # 存贮所有的特征向量数据，最后的形状应该是 N(=1002)*DCT(=13)*L(=每个的长度)
    max_length = 0  # LL#
    # 判断mfcc_length.csv文件是否存在，存在就删除进行重写(存储这个给人看，看看原始数据是怎样的数据格式)
    dataFilePath = './mid_data'
    dataFileName = 'mfcc_length.csv'
    dataFileState = checkFile(dataFilePath, dataFileName)
    if dataFileState:
        os.remove("./mid_data/mfcc_length.csv")
    for i in trainSetFile:
        print(i)
        y, sr = librosa.load(i)
        # 数据格式为二维矩阵：13维 * N列（长度不一样）
        mfcc = librosa.feature.mfcc(y, sr, n_mfcc=n_mfcc)
        # 写入wav文件的mfcc至字典中
        wavmfcc[i] = mfcc.tolist()
        # 将所有文件对应的mfcc vector按序追加到mfcc_list里面
        mfcc_list.append(wavmfcc[i])
        # 每次迭代更新最大的vector长度
        max_length = max(max_length, len(wavmfcc[i][0]))  # 随机训练集文件的最大长度
        # 导出mfcc_length.csv文件，方便直接查看语音数据特征
        # 字典中的key值即为csv中列名
        dataframe = pandas.DataFrame({'filename': i, 'number': len(
            wavmfcc[i]), 'length': len(wavmfcc[i][0])}, index=[0])
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        # dataframe.to_csv("C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/mid_data/mfcc_length.csv",mode='a',header=None,index=False,sep=',')
        dataframe.to_csv("./mid_data/mfcc_length.csv", mode='a',
                         header=None, index=False, sep=',')
        pass
    return wavmfcc, mfcc_list, max_length
    pass

## 获取所有labels的corb值
# 输入：字典集合（嵌套字典）,文件集合（绝对路径）
# 输出：corb数组


def get_label_corb(dictClass, fileClass):
    corbList = []
    # 遍历取出文件
    for i in fileClass:
        # 查看字典中是否有key，取出value
        corb, _, _ = get_y(dictClass, i)
        # 放在列表中
        corbList.append(corb)
    return corbList
    pass

## 将不标准的13*N的矩阵转换为13*MaxN(MaxN：训练集中列最长)


def format_Matrix(diff):
    # 对齐函数，得到扩充的单列表，形状为: diff*1 [0,...]
    replenish = [0 for i in range(diff)]
    return replenish
    pass

# 得到RNN输入 ##batch_data, batch_labels, batch_seqlen


def get_RNN_x(allFilePath, dct, dateset_rate):
    # 查看是否有中间数据文件，有直接加载
    dataFilePath='./mid_data'
    wavmfccFileName="wavmfcc.json"  #这个其实在这运算没什么用，存储来给人看是怎样的数据
    format_mfcc_listFileName="format_mfcc_list.npy"
    mfcc_labelsFileName="mfcc_labels.npy"
    mfcc_length_listFileName="mfcc_length_list.npy"

    wavmfccFileState=checkFile(dataFilePath,wavmfccFileName)
    formatFileState=checkFile(dataFilePath,format_mfcc_listFileName)
    labelsFileState=checkFile(dataFilePath,mfcc_labelsFileName)
    lengthFileState=checkFile(dataFilePath,mfcc_length_listFileName)
    if wavmfccFileState and format_mfcc_listFileName and labelsFileState and lengthFileState:
        # 都存在，直接加载数据（不加载wavmfcc.json，因为不用它计算）
        format_mfcc_list=numpy.load("./mid_data/format_mfcc_list.npy")
        mfcc_labels=numpy.load("./mid_data/mfcc_labels.npy")
        mfcc_length_list=numpy.load("./mid_data/mfcc_length_list.npy")
    else:
        # 返回的是未进行标准化的数据，文件名*13*N（不等长）
        wavmfcc, mfcc_list, max_length = get_mfcc_list(
            allFilePath, dct, dateset_rate)
        # batch_seqlen
        mfcc_length_list = []
        # 遍历每个文件的特征向量
        for vector_i in mfcc_list:
            # 遍历所有的特征向量长度
            each_length = len(vector_i[0])
            # 求出每个文件对应的每个vector的长度，即batch_seqlen
            # mfcc_list是一个3维数组，第一维代表每个文件，第二维是dct的长度，第三维是dct下的每个向量
            # 所以取所有文件,使用:遍历；访问第一个dct的第一个向量
            # 形状为： FileQuantity*1
            mfcc_length_list.append(each_length)
            # 格式化所有的数据，变成固定维度
            if each_length < max_length:
                # 若是长度不够,按照差值进行扩充，这里先生成补充的单列
                replenish = format_Matrix(max_length-each_length)
                # 对每一个vector进行整体扩充
                for k in vector_i:
                    k += replenish
                    pass
                pass
            pass
        # 求出训练集所有labels的corb值
        # 文件集合
        trainSet, _ = divide_dataset(allFilePath, dateset_rate)
        #fileClass = trainSet.tolist()
        fileClass = trainSet
        # 字典集合
        trainSetLabel, _ = get_allFileLabel(allFilePath, dateset_rate)
        dictClass = trainSetLabel
        # corbLabel列表
        mfcc_labels = get_label_corb(dictClass, fileClass)

        # 保存中间数据，方便加载调用
        # 将标准化后的mfcc参数列表转换为numpy.array
        # 形状是:N(=1002)*DCT(=13)*max_length(训练集中最长的数据)
        format_mfcc_list = numpy.array(mfcc_list)
        # mfcc_labels是保存训练集中所有corb的值（0/1）
        mfcc_labels=numpy.array(mfcc_labels)
        # 形状是:N(训练集中的文件个数)*1 记录的是每个vector的实际长度
        mfcc_length_list = numpy.array(mfcc_length_list)
        # 保存npy文件,方便之后计算用
        numpy.save(
            './mid_data/format_mfcc_list.npy', format_mfcc_list)
        numpy.save(
            './mid_data/mfcc_labels.npy', mfcc_labels)
        numpy.save(
            './mid_data/mfcc_length_list.npy', mfcc_length_list)
        # 将字典数据存入json格式文件
        jsonFile = json.dumps(wavmfcc)
        with open('./mid_data/wavmfcc.json', 'w') as file:
            file.write(jsonFile)
        # 输出字典数据的长度，即字典中键值对的数量
        print("wavmfcc")
        print(len(wavmfcc))
    return format_mfcc_list, mfcc_labels, mfcc_length_list
    pass


if __name__ == '__main__':
    # 获取所有wav文件路径
    allFilePath = 'D:/FFOutput'
    dateset_rate = 0.9  # 拆分比率
    # 测试get_mfcc_list函数
    #wavmfcc, mfcc_list, max_length = get_mfcc_list(allFilePath, 13, dateset_rate)
    # 测试get_RNN_x函数
    dct = 13
    format_mfcc_list, mfcc_labels, mfcc_length_list = get_RNN_x(
        allFilePath, dct, dateset_rate)
    # 保存npy文件的形状
    print("format_mfcc_list")
    print(format_mfcc_list.shape)
    print("mfcc_labels")
    print(mfcc_labels.shape)
    print("mfcc_length_list")
    print(mfcc_length_list.shape)
    print("len(mfcc_labels")
    print(len(mfcc_labels))
pass
