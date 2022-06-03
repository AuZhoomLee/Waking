from getWaveSeries import get_waveSeries


# 按序遍历每一个音频数据点，累加求平方
# 输入：某一个音频的时间序列数据，阈值（默认为0）
# 输出：该音频的能量


def get_Energy(waveSeries):
    # 计算音频总能量
    energy = 0.0
    for k in waveSeries:
        if k != 0:
            energy = energy + k * k
        pass
    return energy
    pass


if __name__ == '__main__':
    fileName = "D:/FFOutput/s-2/Lcw/lcw.1.BFN.wav"
    waveSeries = get_waveSeries(fileName)
    energy = get_Energy(waveSeries)
    print(energy)
    pass
