import matplotlib.pyplot as plt
import numpy as np
import os
import json
from getY import get_mark

##yorn test##

    # plot the wave gragh
X = np.load("X.npy")
Y = np.load("Y.npy")
N = np.load("N.npy")
#plt.figure(1)#全范围Y，N分布散点图
#for i in range(Y.shape[0]):
#        Yy=Y[i,:]
#        plt.plot(X,Yy,'r.')
#for i in range(N.shape[0]):
#        Nn=N[i,:]
#        plt.plot(X,Nn,'b.')
#plt.xlabel("k")
#plt.ylabel("N")
#plt.title("YorN distribution")
#plt.show()
ymax = np.load("Ymax.npy")
ymin = np.load("Ymin.npy")
ymean = np.load("Ymean.npy")
nmax = np.load("Nmax.npy")
nmin = np.load("Nmin.npy")
nmean = np.load("Nmean.npy")
#plt.figure(2)#Y,N统计意义计数图
#plt.subplot(211)
#plt.xlabel("k")
#plt.ylabel("N")
#plt.title("Statistical YorN distribution")
#plt.plot(X,ymax,'g^',linewidth=0.1,label='Ymax')
#plt.plot(X,ymin,'gv',linewidth=0.1,label='Ymin')
#plt.plot( X,ymean,'g',linewidth=1,label='Ymean')
#plt.plot( X,nmax,'r^',linewidth=0.1,label='Nmax')
#plt.plot(X,nmin,'rv',linewidth=0.1,label='Nmin')
#plt.plot(X,nmean,'r',linewidth=1,label='Nmean')
#plt.legend(loc='upper right')
#plt.subplot(212)
#plt.xlabel("k")
#plt.ylabel("N")
#plt.title("Means of YorN distribution")
#plt.plot( X,ymean,'g',linewidth=1,label='Ymean')
#plt.plot(X,nmean,'r',linewidth=1,label='Nmean')
#plt.legend(loc='upper right')
#plt.show()
delta = nmean - ymean
print(delta.shape)
ok = 0.0
md = 0
for i in X:
    if i > 0.01:          #控制查找范围，在稀疏的高平频分离无意义
        x = int(i * 1000)
        if md < delta[x]: #找到局部最优且最大的长度值
            md = delta[x]
            ok = i             #返回此刻的横坐标索引 k
            #0.02 9277.826351351352
print(ok,md)
plt.figure(3)
plt.xlabel("k")
plt.ylabel("Difference")
plt.plot(X,delta,'-',linewidth=1,label='Difference')
plt.scatter([ok,],[md,],color='red',linewidth=0.5)
plt.plot([ok,ok],[0,md],50,color='blue',linestyle="--",linewidth=0.7)
plt.legend(loc='upper right')
plt.annotate('local maximum D=9277.826351351352',xy=(ok,md),xytext=(0.025,10000),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.annotate('optimal k=0.02',xy=(ok,0),xytext=(0.025,100),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.title("Difference curve")

ok = 0.02
ox = int(ok * 1000)
Yo = int(ymean[ox])
No = int(nmean[ox])
print(No,Yo)

#定义求距离函数
def get_dis(x,o):
    return x - o

#定义求R值函数
def get_R(dis,p):
    if dis >= 0:#x若高于o，即在o的上邻域，概率为1-p
        return dis / (1 - p)
    else: #x若低于o，即在o的下邻域，概率为p
        return abs(dis) / p

Nx = N[:,ox]
Yx = Y[:,ox]
print(Nx.shape,Yx.shape)
np.save('Nx',Nx)
np.save('Yx',Yx)
#print(Nx,Yx)
def yorn(Length,k,y,n,p):
    ydis = get_dis(Length,y) #求出距Y中心点的标量
    yr = get_R(ydis,p) #求出分类为Y的R值
    ndis = get_dis(Length,n) #求出距N中心点的标量
    nr = get_R(ndis,p)#求出分类为N的R值
    if yr < nr: #若分类为Y的R小于等于N则分类为Y:1
        return 1
    else : #若分类为N的R小于Y则分类为N:0
        return 0

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

Ay = get_Accu(Yx,1,0.02,Yo,No,0.5)
An = get_Accu(Nx,0,0.02,Yo,No,0.5)
print("Testing Accuracy")
print("Y:",Ay)
print("N:",An)
plt.show()

###get_x test##
'''
E=np.load("E.npy")
L=np.load("L.npy")
#print(E.shape,L.shape)
Emax=np.amax(E,0)
Emin=np.amin(E,0)
Emean=np.mean(E,0)
print(Emax,Emin,Emean)
#4,614 159  1,519 
filepath="E:/FFOutput/sound1/"
filename= os.listdir(filepath)
n=0
#for i in filename:
#    print(i,',',L[n])
#    n=n+1

Lmax=np.amax(L,0)
Lmin=np.amin(L,0)
Lmean=np.mean(L,0)
print(Lmax,Lmin,Lmean)
#401,442 41,267 137,346 
'''