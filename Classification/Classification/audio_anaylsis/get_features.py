# coding: utf-8
import librosa
import numpy as np
import json
import matplotlib.pyplot as plt
from get_filename import get_filename


def get_features(wavepath):
    path = get_filename(wavepath)
    Fhz = []
    fhz = {}
    fm = 0
    for i in path:
        y,sr = librosa.load(i)
        #使用roll_percent = 0.85（默认值）近似最大频率
        f = librosa.feature.spectral_rolloff(y,sr)
        #print(type(f),len(f[0]),f)

        #plt.figure()
        #plt.subplot(2,1,1)
        #plt.title("Roff-off frequency graph of "+i)
        #plt.semilogy(f.T,label='Roll-off frequency')
        #plt.ylabel('Hz')
        #plt.xticks([])
        #plt.xlim([0,f.shape[-1]])
        #plt.legend()
        #plt.grid('on')
        #plt.show()
        for i in f:
            fm+=(i * i)
        fm = sqrt(fm)
        fhz[i] = f.tolist()
        Fhz.append(f.tolist())
    F = np.array(Fhz)
    np.save('F',F)
    print(F.shape)
    return  fm,fhz

if __name__ == '__main__':
    filepath = "D:/FFOutput/sound1/" 
    fm,rolloff = get_features(filepath)
    #print('fhz')
