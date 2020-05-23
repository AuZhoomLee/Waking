import os
import pandas

#这个是带子文件夹的取出所有.wav后缀文件名字

def get_filename(path, rule):
    all = []
    for fpathe,dirs,fs in os.walk(path):   # os.walk获取所有的目录
        for f in fs:
            filename = os.path.join(fpathe,f)
            if filename.endswith(rule):  # 判断是否是".wav"结尾
                all.append(filename)
    return all

  
if __name__ == '__main__':
    wavdir = 'D:/FFOutput/'
    rule = ".wav"
    filename = get_filename(wavdir,rule)
    #print(type(filename))
    #count = 0
    #for i in filename:
    #    count = count + 1
    #    print(count,i)

    #字典中的key值即为csv中列名
    dataframe = pandas.DataFrame({'':filename})

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("./data/wav/get_alldir_filename.csv",header=None,index=False,sep=',')

