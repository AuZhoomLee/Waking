from get_waveSeries import get_waveSeries

# 按序遍历每一个音频数据点，若大于某一阈值就计数
# 输入：某一个音频的时间序列数据，阈值（默认为0）
# 输出：该音频的有声段长度


def get_length(waveSeries):
    # 求出有声段长度
    wavelength = 0
    for j in waveSeries:        # if j >= theshold :      #theshold 是一个阈值 大于it表示是人声发音，小于it是环境发声
        if j != 0:              # 现今是统计了音频数据不等于0时计数长度，然而实际情况一般都是先去噪，然后大于环境阈值才是真正有声长度
            wavelength = wavelength + 1
        pass
    return wavelength
    pass


if __name__ == '__main__':
    fileName = "D:/FFOutput/s-2/Lcw/lcw.1.BFN.wav"
    waveSeries = get_waveSeries(fileName)
    waveLength = get_length(waveSeries)
    print(waveLength)
    pass
