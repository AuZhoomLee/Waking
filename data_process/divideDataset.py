import numpy as np
from check import checkFile
from get_alldir_filename import get_filename

## 将所有文件绝对路径划分为训练集和测试集
# 输入：所有文件的根文件夹（可以含子文件夹）、划分率
# 输出：numpy.ndarray格式的训练集和测试集


def divide_dataset(allFilePath, dateset_rate):
    all_FileName = get_filename(allFilePath)
    # print(allFileName)
    # print(type(allFileName))
    # 判断是否已经进行拆分，已拆分就直接调用数据
    dataFilePath = './mid_data'
    trainSetFile = 'trainSet.npy'
    testSetFile = 'testSet.npy'
    state_trainSet = checkFile(dataFilePath, trainSetFile)
    state_testSet = checkFile(dataFilePath, testSetFile)
    if state_trainSet and state_testSet:
        print("===================LoadFile=========================\n")
        trainSet = np.load("./mid_data/trainSet.npy")
        testSet = np.load("./mid_data/testSet.npy")
    else:
        # 按比率拆分成两个列表：训练集、测试集
        allFileName = np.array(all_FileName)
        fileNum = allFileName.shape[0]
        trainNum = int(fileNum * dateset_rate)
        trainSetIndex = np.random.choice(fileNum, trainNum, replace=False)
        trainSet = allFileName[trainSetIndex]  # 训练集
        testSetIndex = np.arange(fileNum)
        testSetIndex = np.delete(testSetIndex, trainSetIndex)
        testSet = allFileName[testSetIndex]
        # 保存拆分后的数据
        np.save("./mid_data/trainSet.npy", trainSet)
        np.save("./mid_data/testSet.npy", testSet)
    return trainSet, testSet
pass


if __name__ == '__main__':
    # 获取所有wav文件路径
    allFilePath = 'D:/FFOutput'
    dateset_rate = 0.9  # 拆分比率

    trainSet, testSet = divide_dataset(allFilePath, dateset_rate)
    print("trainSet===>", trainSet)
    print("testSet===>", testSet)
    print("trainSet[0]===>", trainSet[0])
    print("testSet[0]===>", testSet[0])
    # 输出文件个数
    print("len(trainSet):", len(trainSet))
    print("len(testSet):", len(testSet))
    # 判断是否存在交集
    # 转换为集合使用intersection()方法
    trainSet = set(trainSet)
    testSet = set(testSet)
    fileUnite = trainSet.intersection(testSet)
    print("fileUnite:", fileUnite)
pass
