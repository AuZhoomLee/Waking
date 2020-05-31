import wave
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from get_y import get_mark
from check import checkFile
from divide_dataset import divide_dataset
from get_alldir_filename import get_filename

# 定义训练函数求解最优分离k与Y/N的分离中心点


def get_opt(filepath, dateset_rate, learnrate, finalvalue):
    # 判断文件夹下是否存在文件，存在就跳过，不存在就保存
    dataFilePath = './mid_data'
    file_X = 'X.npy'
    file_Y = 'Y.npy'
    file_N = 'N.npy'
    state_X = checkFile(dataFilePath, file_X)
    state_Y = checkFile(dataFilePath, file_Y)
    state_N = checkFile(dataFilePath, file_N)
    if state_X == True and state_Y == True and state_N == True:
        print("exist file:", file_X, file_Y, file_N)
        X = np.load("./mid_data/X.npy")
        Y = np.load("./mid_data/Y.npy")
        N = np.load("./mid_data/N.npy")
    else:
        # 参数分别为：训练数据目录，学习率，统计终止值（一般在0.2后Y/N不在分离）
        # 文件需要取到包含子文件夹下的所有wav格式文件
        # 使用随机划分后的训练集
        # filename = get_filename(filepath)
        trainSet, _ = divide_dataset(filepath, dateset_rate)
        filename = trainSet
        y = []
        n = []
        count = 0
        for i in filename:
            f = wave.open(i, 'rb')
            # 测试===》读取的真实路径
            print("===>>>filepath:", i)
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)
            waveData = np.frombuffer(strData, dtype=np.int16)
            waveData = waveData * 1.0 / (max(abs(waveData)))
            # 测试===》
            print("waveData===>", waveData)
            k = 0.0
            l = []

            # 这里需要将文件名转换（小写==》大写），再到get_mark中进行匹配
            turnI = i.upper()
            mark = int(get_mark(turnI)[2])
            print("mark===>>>", mark)
            while k < finalvalue:
                nk = 0
                for j in waveData:  # 遍历音频数据中每个声谱
                    if abs(j) >= k:  # 若绝对值大于k值则计数长度
                        nk = nk + 1
                l.append(nk)  # 横向加入数组
                k = k + learnrate  # learnrate为递增率
            if mark > 0:  # 1标记为“是”
                y.append(l)
            else:  # 0标记为“不是”
                n.append(l)
            count = count + 1
            print(count, i, ',', mark, len(l))
        Y = np.array(y)
        N = np.array(n)
        X = np.arange(0, finalvalue, learnrate)
        np.save('./mid_data/X.npy', X)
        np.save('./mid_data/Y.npy', Y)
        np.save('./mid_data/N.npy', N)
        pass
    # plot the wave gragh
    plt.figure(1)  # 全范围Y，N分布散点图
    for i in range(Y.shape[0]):
        Yy = Y[i, :]
        plt.plot(X, Yy, 'r.')
    for i in range(N.shape[0]):
        Nn = N[i, :]
        plt.plot(X, Nn, 'b.')
    plt.xlabel("k")
    plt.ylabel("N")
    plt.title("YorN distribution")
    plt.show()

    plt.figure(2)  # Y,N统计意义计数图
    ymax = np.amax(Y, 0)
    ymin = np.amin(Y, 0)
    ymean = np.mean(Y, 0)
    nmax = np.amax(N, 0)
    nmin = np.amin(N, 0)
    nmean = np.mean(N, 0)
    plt.subplot(211)  # 最大，最小，最佳概率统计图
    plt.xlabel("k")
    plt.ylabel("N")
    plt.title("Statistical YorN distribution")
    plt.plot(X, ymax, 'g^', linewidth=0.1, label='Ymax')
    plt.plot(X, ymin, 'gv', linewidth=0.1, label='Ymin')
    plt.plot(X, ymean, 'g', linewidth=1, label='Ymean')
    plt.plot(X, nmax, 'r^', linewidth=0.1, label='Nmax')
    plt.plot(X, nmin, 'rv', linewidth=0.1, label='Nmin')
    plt.plot(X, nmean, 'r', linewidth=1, label='Nmean')
    plt.legend(loc='upper right')
    plt.subplot(212)  # 最佳概率统计直观图
    plt.xlabel("k")
    plt.ylabel("N")
    plt.title("Means of YorN distribution")
    plt.plot(X, ymean, 'g', linewidth=1, label='Ymean')
    plt.plot(X, nmean, 'r', linewidth=1, label='Nmean')
    plt.legend(loc='upper right')
    plt.show()

    delta = nmean - ymean
    print(delta.shape)

    ok = 0.0
    md = 0
    for i in X:
        if i > 0.01:  # 控制查找范围，在稀疏的高平频分离无意义
            x = int(i * 1000)
            if md < delta[x]:  # 找到局部最优且最大的长度值
                md = delta[x]
                ok = i  # 返回此刻的横坐标索引 k
    print("ok==>", ok, "md==>", md)
    # 上段程序(300)求得到的坐标为：0.02 9277.826351351352

    # 上段程序(1002个数据)求得到的坐标为：ok==> 0.018000000000000002 md==> 8600.688151394424
    plt.figure(3)  # 差值曲线，求解最优极大值
    plt.xlabel("k")
    plt.ylabel("Difference")
    plt.plot(X, delta, '-', linewidth=1, label='Difference')
    plt.scatter([ok, ], [md, ], color='red', linewidth=0.5)
    plt.plot([ok, ok], [0, md], 50, color='blue',
             linestyle="--", linewidth=0.7)
    plt.legend(loc='upper right')
    plt.annotate('local maximum D=8600.688151394424', xy=(ok, md), xytext=(0.025, 10000), arrowprops=dict(arrowstyle="->",
                                                                                                          connectionstyle="arc3,rad=.2"))
    plt.annotate('optimal k=0.018', xy=(ok, 0), xytext=(0.025, 100), arrowprops=dict(arrowstyle="->",
                                                                                     connectionstyle="arc3,rad=.2"))
    plt.show()

    # 求得最优k取值的Y,N最佳概率分离点
    ox = int(ok * 1000)
    Yo = int(ymean[ox])
    No = int(nmean[ox])
    print("No==>", No, "Yo==>", Yo)
    # 保存一些计算数据，进行判断，有就不保存
    file_ymax = 'ymax.npy'
    file_ymin = 'ymin.npy'
    file_ymean = 'ymean.npy'
    file_nmax = 'nmax.npy'
    file_nmin = 'nmin.npy'
    file_nmean = 'nmean.npy'
    file_delta = 'delta.npy'
    state_ymax = checkFile(dataFilePath, file_ymax)
    state_ymin = checkFile(dataFilePath, file_ymin)
    state_ymean = checkFile(dataFilePath, file_ymean)
    state_nmax = checkFile(dataFilePath, file_nmax)
    state_nmin = checkFile(dataFilePath, file_nmin)
    state_nmean = checkFile(dataFilePath, file_nmean)
    state_delta = checkFile(dataFilePath, file_delta)
    if state_ymax and state_ymin and state_ymean and state_nmax and state_nmin and state_nmean and state_delta:
        print("file exist:", state_ymax, state_ymin, state_ymean,
              state_nmax, state_nmin, state_nmean, state_delta)
    else:
        np.save('./mid_data/ymax.npy', ymax)
        np.save('./mid_data/ymin.npy', ymin)
        np.save('./mid_data/ymean.npy', ymean)
        np.save('./mid_data/nmax.npy', nmax)
        np.save('./mid_data/nmin.npy', nmin)
        np.save('./mid_data/nmean.npy', nmean)
        np.save('./mid_data/delta.npy', delta)
    return ox, Yo, No


pass

# 定义求距离函数


def get_dis(x, o):
    return x - o


pass

# 定义求R值函数


def get_R(dis, p):
    if dis >= 0:  # x若高于o，即在o的上邻域，概率为1-p
        return dis / (1 - p)
    else:  # x若低于o，即在o的下邻域，概率为p
        return abs(dis) / p


pass

# 定义分类Y/N函数


def yorn(Length, k, y, n, p):
    ydis = get_dis(Length, y)  # 求出距Y中心点的标量
    yr = get_R(ydis, p)  # 求出分类为Y的R值
    ndis = get_dis(Length, n)  # 求出距N中心点的标量
    nr = get_R(ndis, p)  # 求出分类为N的R值
    if yr <= nr:  # 若分类为Y的R小于等于N则分类为Y:1
        return 1
    else:  # 若分类为N的R小于Y则分类为N:0
        return 0


pass

# 定义求分类准确率的函数


def get_Accu(X, yn, k, y, n, p):
    # 参数：长度列，预先标记，最优分界k，Y分类中心点y，N分类中心点n，分类概率p
    yes = 0
    no = 0
    for i in X:
        cf = yorn(i, k, y, n, p)
        if cf == yn:
            yes = yes + 1
        else:
            no = no + 1
    return yes / (yes + no)


pass

if __name__ == '__main__':
    #wavdir = 'D:/TestTrain/'
    # 获取所有wav文件路径
    allFilePath = 'D:/FFOutput'
    dateset_rate = 0.9  # 拆分比率
    # 测试训练代码
    ox, Yo, No = get_opt(allFilePath, dateset_rate, 0.001, 0.2)
    k = ox / 1000
    print("k===>", k)
    Y = np.load("./mid_data/Y.npy")
    N = np.load("./mid_data/N.npy")
    Nx = N[:, ox]
    Yx = Y[:, ox]
    print(Nx.shape, Yx.shape)
    # 测试精确度
    Ay = get_Accu(Yx, 1, k, Yo, No, 0.5)
    An = get_Accu(Nx, 0, k, Yo, No, 0.5)
    print("Testing Accuracy:")
    print("Y:", Ay)
    print("N:", An)
pass
