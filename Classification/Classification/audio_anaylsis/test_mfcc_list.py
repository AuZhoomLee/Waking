# coding: utf-8
import librosa
import numpy
import pandas
import json
from get_y import get_mark
from get_alldir_filename import get_filename

def get_mfcc_list(wavpath,n_mfcc):
    path = get_filename(wavpath,rule)
    #测试输出
    #print(path)
    wavmfcc = {}
    mfccData = []       #LL#
    mfcc_list=[] #存贮所有的特征向量数据，最后的形状应该是 N(=1002)*DCT(=13)*L(=每个的长度)
    max_length=0   #LL#
    for i in path:
        y,sr = librosa.load(i)
        mfcc = librosa.feature.mfcc(y,sr,n_mfcc=n_mfcc)
        #写入wav文件的mfcc至字典中
        wavmfcc[i] = mfcc.tolist()
        #将所有文件对应的mfcc vector按序追加到mfcc_list里面
        mfcc_list.append(wavmfcc[i])
        #每次迭代更新最大的vector长度
        max_length=max(max_length,len(wavmfcc[i][0])) #1002个文件最大长度最后为223
        
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

        #mfccData[i] = numpy.append(mfcc)          #LL#
        #LL#可以在这里同步计算最大长度
        #max_length=max(max_length,wavmfcc[i])

        # print(type(wavmfcc))
        # [
        # [[],[]],
        # [[],[]]
        # ]
        '''
        ==============================测试段=====================
        '''

        '''
        导出mfcc_length.csv文件
        方便直接查看语音数据特征
        '''
        #print(i,",",len(wavmfcc[i]),",",len(wavmfcc[i][0]))
        #字典中的key值即为csv中列名
        dataframe = pandas.DataFrame({'filename':i,'number':len(wavmfcc[i]),'length':len(wavmfcc[i][0])},index=[0])
        #将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv("C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/mid_data/mfcc_length.csv",mode='a',header=None,index=False,sep=',')        
        pass
    #测试一下生成
    print(max_length)
    print(mfcc_list)
    #生成npy文件 
    #LL#这个地方暂时不能使用wavmfcc来存储，是以字典的形式只存储一条
    #LL#numpy.save('./mid_data/mfcc.npy',wavmfcc)
    #wavmfcc是字典，在ifmain里需要，mfcc_list是一个列表，max_length就是一个整数
    #wavmfcc的keys包含的是 文件名，values包含了所有的 mfcc vecotr
    return wavmfcc,mfcc_list,max_length

# D:\Code\Tmall Genie\Classification\Classification.pyproj

def format_Matrix(diff):
    #对齐函数，得到扩充的单列表，形状为: diff*1 [0,...]
    replenish=[0 for i in range(diff)]
    return replenish

#得到RNN输入 ##batch_data, batch_labels, batch_seqlen
def get_RNN_x(wavpath,dct):
    #mfcc由get_mfcc_list返回后是一个列表
    wavmfcc,mfcc_list,max_length=get_mfcc_list(wavpath,n_mfcc=dct)
    #batch_seqlen
    mfcc_length_list = []
    #遍历每个文件的特征向量
    for vector_i in mfcc_list:
        #遍历所有的特征向量长度
        each_length=len(vector_i[0])
        ##求出每个文件对应的每个vector的长度，即batch_seqlen
        ##mfcc_list是一个3维数组，第一维代表每个文件，第二维是dct的长度，第三维是dct下的每个向量
        ##所以取所有文件,使用:遍历；访问第一个dct的第一个向量
        ##形状为： FileQuantity*1
        mfcc_length_list.append(each_length)
        #格式化所有的数据，变成固定维度
        if each_length<max_length:
            #若是长度不够,按照差值进行扩充，这里先生成补充的单列
            replenish=format_Matrix(max_length-each_length)
            #对每一个vector进行整体扩充
            for k in vector_i:
                k+=replenish
                pass
            pass
        pass
    
    #转换所有的列表为numpy.array
    mfcc=numpy.array(mfcc_list) #形状是:N(=1002)*DCT(=13)*max_length(=223)
    mfcc_length=numpy.array(mfcc_length_list) #形状是:N(=1002)*1 记录的是每个vector的实际长度

    #保存npy文件
    print("mfcc")
    print(mfcc.shape)
    print("mfcc_length")
    print(mfcc_length.shape)

    #保存npy文件,方便之后计算用
    numpy.save('C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/mid_data/mfcc.npy',mfcc)
    numpy.save('C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/mid_data/mfcc_length.npy',mfcc_length)


    ##如果已经提取完成全部的mfcc，直接调用原来保存的
    #mfcc=np.load("./mid_data/mfcc.npy")

    ##求出所有的labels
    ##get_y返回一个字典,取所有文件的对应编码的第一位
    ##形状为： FileQuantity*1
    #mfcc_labels=numpy.array(int(get_y(wavpath)[:][0]))
    #改一下试试 get_y返回：y,ty,corb,torf,yorn
    all_filename=wavmfcc.keys() #得到所有的文件名
    file_label=[]
    for i in all_filename:
        #遍历所有的文件名
        i=i.upper()#转换为大写
        #print(i)
        code = get_mark(i) #提取所有的标记按照二进制形式返回
        file_label.append(int(code[0])) #BTN 010 code ="010" ->code[0]="0"->int(code[0])=0
        pass
    #测试输出
    mfcc_labels=numpy.array(file_label)
    print("mfcc_labels")
    print(mfcc_labels.shape)
    numpy.save('C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/mid_data/mfcc_labels.npy',mfcc_labels)
    
    return mfcc,mfcc_labels,mfcc_length

def test_get_labels(wavpath,rule):
    path = get_filename(wavpath,rule)
    print(len(path))
    file_label=[]
    for i in path:
        i=i.upper()
        print(i)
        code = get_mark(i) #提取所有的标记按照二进制形式返回
        print(code)
        file_label.append(int(code[0])) #BTN 010 code ="010" ->code[0]="0"->int(code[0])=0
        pass
    mfcc_labels=numpy.array(file_label)
    print(mfcc_labels.shape)
    pass

if __name__=='__main__':
    wavpath = "C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/FFOutput/" 
    rule= ".wav"
    #wavmfcc,mfc#,_=get_mfcc_list(wavpath,13)

    ##测试目录下文件mfc#输出
    ##for i in wa#mfcc.keys():
    # print(i#len(wavmfcc[i]),len((wavmfcc[i][0])))
    #'''
    #将#有的wav文件进行#FCC参数提取，M*13维度矩阵
    #并以字典格式数据存储在#fcc_list.json中
    #'''
    ###存到./mid_d#ta下
    #ideafile = #D:/Code/Tmall Genie/Classification/mid_data/mfcc_list.json"
    #json_str = #son.dumps(wavmfcc,indent=4)
    #with open(i#eafile,'w') as f:
    #    f.write#json_str)
    ##LL#需要测试输出一#             mfcc 这个列表的形状，这个列表只包含了所有的数据，形状应该是N*DCT(=13)*L
    ##LL# print(#en(mfcc),len(mfcc[0]),len(mfcc[0][0])) ##预计的输出应该是 1002 13 57

    ##
    get_RNN_x(wavpath,dct=13)
    #test_get_labels(wavpath,rule)
    pass
