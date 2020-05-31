import os
import pandas

#带子文件夹,取出所有.wav后缀文件名字==》绝对路径
def get_filename(path):
    rule = ".wav"
    all = []
    for parent,dirnames,filenames in os.walk(path):   # os.walk获取所有的目录
        for f in filenames:
            filename = os.path.join(parent,f)
            if filename.endswith(rule):  # 判断是否是".wav"结尾
                filename = filename.replace('\\','/')
                all.append(filename)
    return all

  
if __name__ == '__main__':
    wavdir = 'D:/TestTrain/'
    
    filename = get_filename(wavdir)
    #print(type(filename))
    #count = 0
    #for i in filename:
    #    count = count + 1
    #    print(count,i)
    
    #测试生成csv文件
    ##字典中的key值即为csv中列名
    #dataframe = pandas.DataFrame({'':filename})

    ##将DataFrame存储为csv,index表示是否显示行名，default=True
    #dataframe.to_csv("./data/wav/get_alldir_filename.csv",header=None,index=False,sep=',')

    #测试
    print(filename)