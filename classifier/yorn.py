import wave
import numpy as np
from LDA import get_opt


#定义求长度函数
def get_length(filepath,k):
    f = wave.open(filepath,'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    waveData = np.frombuffer(strData,dtype=np.int16)
    waveData = waveData * 1.0 / (max(abs(waveData)))
    Length = 0
    for i in waveData:
        if abs(i) >= k:
            Length = Length + 1
    return Length
    pass

#定义求距离函数
def get_dis(x,o):
    return x - o

#定义求R值函数
def get_R(dis,p):
    if dis >= 0:#x若高于o，即在o的上邻域，概率为1-p
        return dis / (1 - p)
    else: #x若低于o，即在o的下邻域，概率为p
        return abs(dis) / p

#定义分类Y/N函数
def yorn(Length,k,y,n,p):
    ydis = get_dis(Length,y) #求出距Y中心点的标量
    yr = get_R(ydis,p) #求出分类为Y的R值
    ndis = get_dis(Length,n) #求出距N中心点的标量
    nr = get_R(ndis,p)#求出分类为N的R值
    if yr <= nr: #若分类为Y的R小于等于N则分类为Y:1
        return 1
    else : #若分类为N的R小于Y则分类为N:0
        return 0

#定义文件读取返回分类函数
def wav_yorn(filepath,k,y,n,p):#参数分别为：文件路径，最优分界k，Y分类中心点y，N分类中心点n，分类概率p
    Length = get_length(filepath,k) #先求最优k分界的长度
    return yorn(Length,k,y,n,p)


if __name__ == '__main__':
    #对输入的wav数据进行Y/N分类测试
    wavdir = 'D:/FFOutput/'     #训练数据
    dateset_rate = 0.9  # 拆分比率
    wavFilePath = 'D:/TestTrain/Test/sj.bfy.1.wav'      #测试数据
    ox,y,n = get_opt(wavdir,dateset_rate,0.001,0.2)
    k = ox / 1000
    p = 0.5
    testState = wav_yorn(wavFilePath,k,y,n,p)
    print("wavFile===>>>",wavFilePath)
    print("Y/N分类===>>>testState:",testState)
    pass