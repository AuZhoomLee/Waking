import os


def checkFile(filePath, fileName):
    # 获取文件路径下的所有文件名
    allFileName = os.listdir(filePath)
    # 在指定路径下，判断是否存在指定文件
    for file in allFileName:
        # 输出所有文件和文件夹
        # print("existFile:==>",file)
        if file == fileName:
            # print("file:",file)
            # print("fileName:",fileName)
            fileState = True
            break
        else:
            fileState = False
    # 判断是否存在某文件（默认路径下）
    # 只能判断默认路径下存在的文件./
    # fileState = os.path.exists(fileName)
    return fileState


pass

if __name__ == '__main__':
    # 测试
    filePath = './mid_data_test'
    fileName = 'mfcc_list.json.npy'
    fileState = checkFile(filePath, fileName)
    print(fileState)
    pass
