import librosa

# 求一个wav文件的滚降频率
# 输入：文件名(绝对路径)
# 输出：滚降频率

def get_Frequency(fileName):
    y, sr = librosa.load(fileName)
    # Approximate maximum frequencies with roll_percent=0.85 (default)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    return rolloff
    pass

if __name__ == '__main__':
    fileName = "D:/FFOutput/s-2/Lcw/lcw.1.BFN.wav"
    rolloff = get_Frequency(fileName)
    print(rolloff)
