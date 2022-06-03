import json

from check import checkFile

from divideDataset import divide_dataset


def StaticLengthNumber(str_number, length):  # 函数主要将二进制数转为编码字符串
    str_number = str(str_number)
    while (len(str_number) < length):
        str_number = '0' + str_number
    return str_number


pass


def get_mark(filename):
    code = ""
    mark = ["BFN", "BFY", "BTN", "BTY", "CFN", "CFY", "CTN", "CTY"]
    # C1B0 F0T1 N0Y1
    # 唯一编码，分别从‘000’按序递增到‘111’
    # d.1.BTN.wav, 010=y[0] y[0]的type 是str, if y[0][1]='1' : 代表T int(y[i][2])>0
    # 代表yes else 代表不是N
    for j in mark:
        if j in filename:
            b = bin(mark.index(j)).replace('0b', '')
            # 测试===》
            # print("b===>",b)
            # print("type(b)===>",type(b))
            code = StaticLengthNumber(b, 3)
            # print("code===>",code)
            # print("type(code)===>",type(code))
            break
    return code


pass


# 写一个将数据文件的标记转换成字典存储
# 参考格式：
# dict = {
#        'file1':{
#                'corb':1,
#                'torf':0,
#                'yorn':0},
#        'file2':{
#                'corb':1,
#                'torf':0,
#                'yorn':0},
#        'file3':{
#                'corb':1,
#                'torf':0,
#                'yorn':0},
#        }

# 获取所有文件的标记：训练集、测试集。使用字典存储

def get_allFileLabel(allFilePath, dateset_rate):
    # 如果进行过运算，并且保留有json格式的文件，就直接加载
    dictFilePath = './mid_data'
    trainSetFileName = 'trainSetLabel.json'
    testSetFileName = 'testSetLabel.json'
    trainSetFileState = checkFile(dictFilePath, trainSetFileName)
    testSetFileState = checkFile(dictFilePath, testSetFileName)
    if trainSetFileState and testSetFileState:
        # 加载训练集的JSON格式数据并转换为字典
        with open('./mid_data/trainSetLabel.json', 'r', encoding='UTF-8') as f:
            trainSetLabel = json.load(f)
        # 加载测试集的JSON格式数据并转换为字典
        with open('./mid_data/testSetLabel.json', 'r', encoding='UTF-8') as f:
            testSetLabel = json.load(f)
    else:
        # 调用函数传入划分后的训练集合；
        trainSetFile, testSetFile = divide_dataset(allFilePath, dateset_rate)
        # 训练集
        trainSetLabel = {}  # 存放文件名和文件标记的字典
        for i in trainSetFile:
            j = i.upper()  # 将所有文件名转为大写(只是为了提取标签，不改变绝对路径)
            code = get_mark(j)  # 将标签提取出来，用字符串表示
            # 构建嵌套字典存储
            d1_trainSet = trainSetLabel.setdefault(i, {})
            # 将标签标记的3个参数分离,分别存入嵌套字典
            d2_trainSet = d1_trainSet.setdefault('corb', int(code[0]))
            d2_trainSet = d1_trainSet.setdefault('torf', int(code[1]))
            d2_trainSet = d1_trainSet.setdefault('yorn', int(code[2]))
            # 将字典数据存入json格式文件
            jsonFile = json.dumps(trainSetLabel)
            with open('./mid_data/trainSetLabel.json', 'w') as file:
                file.write(jsonFile)
        # 测试集
        testSetLabel = {}  # 存放文件名和文件标记的字典
        for i in testSetFile:
            j = i.upper()  # 将所有文件名转为大写(只是为了提取标签，不改变绝对路径)
            code = get_mark(j)  # 将标签提取出来，用字符串表示
            # 构建嵌套字典存储
            d1_testSet = testSetLabel.setdefault(i, {})
            # 将标签标记的3个参数分离,分别存入嵌套字典
            d2_testSet = d1_testSet.setdefault('corb', int(code[0]))
            d2_testSet = d1_testSet.setdefault('torf', int(code[1]))
            d2_testSet = d1_testSet.setdefault('yorn', int(code[2]))
            # 将字典数据存入json格式文件
            jsonFile = json.dumps(testSetLabel)
            with open('./mid_data/testSetLabel.json', 'w') as file:
                file.write(jsonFile)
    return trainSetLabel, testSetLabel

    pass


# 重写get_y
# 函数传入：所有标签的字典，要查询的文件名
# 函数功能：取出文件名对应在字典中的值
# 函数返回：corb，yorn，torf
#

def get_y(dictLabelData, fileName):
    # 判断文件是否存在字典数据中
    fileState = fileName in dictLabelData
    if fileState:
        # 将字典中的3个参数取出来
        corb = dictLabelData[fileName]["corb"]
        torf = dictLabelData[fileName]["torf"]
        yorn = dictLabelData[fileName]["yorn"]
    else:
        # 标记的状态只有0/1，返回9代表不存在
        corb = torf = yorn = 9
        print(fileName, "isn't exist in Dict !")
    return corb, torf, yorn
    pass


if __name__ == '__main__':
    # filepath = "D:/FFOutput/"
    # get_y(filepath)

    # 测试get_allFileLabel函数
    # 获取所有wav文件路径
    allFilePath = 'D:/FFOutput'
    dateset_rate = 0.9  # 拆分比率
    trainSetLabel, testSetLabel = get_allFileLabel(allFilePath, dateset_rate)
    # print("trainSetLabel:", trainSetLabel)
    # print("==============================================================")
    # print("testSetLabel:", testSetLabel)
    # ====================================
    # 测试get_y函数
    # 存在文件
    fileName = "D:/FFOUTPUT/S-5/DHY/4D.2.CTN.WAV"
    # 不存在文件
    # fileName = "D:/FFOUTPUT/S-5/DHY/4D.20.CTN.WAV"
    dictLabelData = trainSetLabel
    corb, torf, yorn = get_y(dictLabelData, fileName)
    print("corb:", corb)
    print("torf:", torf)
    print("yorn:", yorn)
pass
