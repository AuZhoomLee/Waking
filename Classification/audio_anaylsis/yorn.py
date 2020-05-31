import wave
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from get_y import get_mark

#定义训练函数求解最优分离k与Y/N的分离中心点
def get_opt(filepath,learnrate,finalvalue):
    #参数分别为：训练数据目录，学习率，统计终止值（一般在0.2后Y/N不在分离）
    filename = os.listdir(filepath)
    y = []
    n = []
    count = 0
    for i in filename:
        f = wave.open(filepath + i,'rb')
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)
        waveData = np.frombuffer(strData,dtype=np.int16)
        waveData = waveData * 1.0 / (max(abs(waveData)))
        k = 0.0
        l = []
        mark = int(get_mark(i)[2])
        while k < finalvalue :
            nk = 0
            for j in waveData:       #遍历音频数据中每个声谱
                if abs(j) >= k:            #若绝对值大于k值则计数长度
                    nk = nk + 1
            l.append(nk)                #横向加入数组
            k = k + learnrate                    #learnrate为递增率
        if mark > 0:                       #1标记为“是”
            y.append(l)
        else :                                #0标记为“不是”
            n.append(l)
        count = count + 1
        print(count,i,',',mark,len(l))
    
    # plot the wave gragh
    plt.figure(1)#全范围Y，N分布散点图
    Y = np.array(y)
    N = np.array(n)
    X = np.arange(0,finalvalue,learnrate)
    for i in range(Y.shape[0]):
        Yy = Y[i,:]
        plt.plot(X,Yy,'r.')
    for i in range(N.shape[0]):
        Nn = N[i,:]
        plt.plot(X,Nn,'b.')
    plt.xlabel("k")
    plt.ylabel("N")
    plt.title("YorN distribution")
    plt.show()
    np.save('./mid_data_test/X.npy',X)
    np.save('./mid_data_test/Y.npy',Y)
    np.save('./mid_data_test/N.npy',N)

    plt.figure(2)  #Y,N统计意义计数图
    ymax = np.amax(Y,0)
    ymin = np.amin(Y,0)
    ymean = np.mean(Y,0)
    nmax = np.amax(N,0)
    nmin = np.amin(N,0)
    nmean = np.mean(N,0)
    plt.subplot(211)  #最大，最小，最佳概率统计图
    plt.xlabel("k")
    plt.ylabel("N")
    plt.title("Statistical YorN distribution")
    plt.plot(X,ymax,'g^',linewidth=0.1,label='Ymax')
    plt.plot(X,ymin,'gv',linewidth=0.1,label='Ymin')
    plt.plot(X,ymean,'g',linewidth=1,label='Ymean')
    plt.plot(X,nmax,'r^',linewidth=0.1,label='Nmax')
    plt.plot(X,nmin,'rv',linewidth=0.1,label='Nmin')
    plt.plot(X,nmean,'r',linewidth=1,label='Nmean')
    plt.legend(loc='upper right')
    plt.subplot(212)  #最佳概率统计直观图
    plt.xlabel("k")
    plt.ylabel("N")
    plt.title("Means of YorN distribution")
    plt.plot(X,ymean,'g',linewidth=1,label='Ymean')
    plt.plot(X,nmean,'r',linewidth=1,label='Nmean')
    plt.legend(loc='upper right')
    plt.show()

    delta = nmean - ymean
    print(delta.shape)
    ok = 0.0
    md = 0
    for i in X:
        if i > 0.01:      #控制查找范围，在稀疏的高平频分离无意义
            x = int(i * 1000)
            if md < delta[x]: #找到局部最优且最大的长度值
                md = delta[x]
                ok = i             #返回此刻的横坐标索引 k
    print(ok,md)
    #上段程序求得到的坐标为：0.02 9277.826351351352
    
    plt.figure(3)#差值曲线，求解最优极大值
    plt.xlabel("k")
    plt.ylabel("Difference")
    plt.plot(X,delta,'-',linewidth=1,label='Difference')
    plt.scatter([ok,],[md,],color='red',linewidth=0.5)
    plt.plot([ok,ok],[0,md],50,color='blue',linestyle="--",linewidth=0.7)
    plt.legend(loc='upper right')
    plt.annotate('local maximum D=9277.826351351352',xy=(ok,md),xytext=(0.025,10000),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    plt.annotate('optimal k=0.02',xy=(ok,0),xytext=(0.025,100),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    plt.show()

    #求得最优k取值的Y,N最佳概率分离点
    ox = int(ok * 1000)
    Yo = int(ymean[ox])
    No = int(nmean[ox])
    print(No,Yo)

    return ok,Yo,No

#定义求长度函数
def get_length(filenpath,k):
    f = wave.open(filepath,'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)
    waveData = np.frombuffer(strData,dtype=np.int16)
    waveData = waveData * 1.0 / (max(abs(waveData)))
    Length = 0
    for i in waveData:
        if abs(waveData) >= k:
            Length = Length + 1
    return Length

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

#定义求分类准确率的函数
def get_Accu(X,yn,k,y,n,p):
    #参数：长度列，预先标记，最优分界k，Y分类中心点y，N分类中心点n，分类概率p
    yes = 0
    no = 0
    for i in X:
        cf = yorn(i,k,y,n,p)
        if cf == yn:
            yes = yes + 1
        else :
            no = no + 1
    return yes / (yes + no)

if __name__ == '__main__':
    wavdir = 'D:/FFOutput/TestTrain/'
    k,Yo,No = get_opt(wavdir,0.001,0.2)
    Y = np.load("./mid_data_test/Y.npy")
    N = np.load("./mid_data_test/N.npy")
    Nx = N[:,ox]
    Yx = Y[:,ox]
    print(Nx.shape,Yx.shape)
    Ay = get_Accu(Yx,1,k,Yo,No,0.5)
    An = get_Accu(Nx,0,k,Yo,No,0.5)
    print("Testing Accuracy:")
    print("Y:",Ay)
    print("N:",An)