import wave
import matplotlib.pyplot as plt
import numpy as np
import os
import json
 

def get_x(filepath):
    '''
    nchannels:声道数
    sampwidth:量化位数（byte）
    framerate:采样频率  默认48000
    nframes:采样点数  默认90112
    '''
    Energy = {}
    Ee = []
    Ll = []
    filename = os.listdir(filepath) #得到文件夹下的所有文件名称
    Lenofwave = {}
    x = {}
    flag = 0
    for i in filename:
        flag = flag + 1
        #print(flag,i)
        f = wave.open(filepath + i,'rb')
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)#读取音频，字符串格式
        waveData = np.frombuffer(strData,dtype=np.int16)#将字符串转化为int
        waveData = waveData * 1.0 / (max(abs(waveData)))#wave幅值归一化
        time = np.arange(0,len(waveData)) * (1.0 / framerate)
        x[i] = waveData.tolist()
        #print(len(waveData))
        #time = np.arange(0,nframes)*(1.0 / framerate)
        #print(len(time))
        #print('nframes:',nframes,type(nframes))
        #print('framerate:',framerate,type(framerate))
        #print('waveData:',type(waveData),len(waveData))
        
        ## plot the wave gragh
        
        #plt.plot(time,waveData)
        #plt.xlabel("Time")
        #plt.ylabel("Amplitude")
        #plt.title("Single channel wavedata of "+i)
        #plt.show()
        
        #plt.grid('on')#标尺，on：有，off:无。

        #求出有声段长度
        count = 0
        for j in waveData:        #if j >= theshold :      #theshold 是一个阈值 大于it表示是人声发音，小于it是环境发声
            if j != 0:#现今是统计了音频数据不等于0时计数长度，然而实际情况一般都是先去噪，然后大于环境阈值才是真正有声长度
                count = count + 1
        Lenofwave[i] = count
        Ll.append(count)

        #计算音频总能量
        e = 0.0
        for k in waveData:
            if k != 0:      #if k >= theshold :                   #theshold 是一个阈值 大于it表示是人声发音，小于it是环境发声
                e = e + k * k
        Energy[i] = e
        print(i,',',Energy[i])
        Ee.append(e)

    E = np.array(Ee)
    L = np.array(Ll)
    np.save('E',E)
    np.save('L',L)
    return x,Lenofwave,Energy

if __name__ == '__main__':
    filepath = "D:/FFOutput/sound1/" #添加所有的音频源文件路径
    xdic,lendic,E = get_x(filepath)
    ideafile = "E:/AuZho/Documents/Au.Pieces Landen/Au.Project-s/毕设/Waking/Classification/Classification/data/E.json"       #生成的中间数据
    json_str = json.dumps(E,indent=4)
    with open(ideafile,'w') as f:
        f.write(json_str)
    pass