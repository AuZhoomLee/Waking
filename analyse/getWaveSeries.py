import wave

import numpy as np


# 对音频进行标准化采样分析
# 输入：文件名(绝对路径)
# 输出：音频的时间序列数据


def get_waveSeries(fileName):
    f = wave.open(fileName, 'rb')
    params = f.getparams()
    # 声道，采样宽度，帧速率，帧数，唯一标识，无损
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)  # 读取音频，字符串格式
    waveData = np.frombuffer(strData, dtype=np.int16)  # 将字符串转化为int
    waveData = waveData * 1.0 / (max(abs(waveData)))  # wave幅值归一化
    # print(type(waveData))
    return waveData
    pass


if __name__ == '__main__':
    fileName = "D:/FFOutput/s-2/Lcw/lcw.1.BFN.wav"
    waveSeries = get_waveSeries(fileName)
    print(waveSeries)
    print(waveSeries.shape)
    pass
