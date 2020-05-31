# coding: utf-8
import librosa
import numpy
import json
from get_filename import get_filename

def get_mfcc_list(wavpath,n_mfcc):
    path = get_filename(wavpath)
    wavmfcc = {}
    for i in path:
        y,sr = librosa.load(i)
        mfcc = librosa.feature.mfcc(y,sr,n_mfcc=n_mfcc)
        #写入文件的mfcc至字典中
        wavmfcc[i] = mfcc.tolist()
        print(i,",",len(wavmfcc[i]),",",len(wavmfcc[i][0]))
        pass
    return wavmfcc

# D:\Code\Tmall Genie\Classification\Classification.pyproj

if __name__ == '__main__':
    wavpath = 'D:/FFOutput/'
    wavmfcc = get_mfcc_list(wavpath,13)
    #测试目录下文件mfcc输出并保存到./data下
    for i in wavmfcc.keys():
        print(i,len(wavmfcc[i]),len((wavmfcc[i][0])))
    ideafile = "E:/AuZho/Documents/Au.Pieces Landen/Au.Project-s/毕设/Waking/Classification/Classification/data/mfcc_list.json"
    json_str = json.dumps(wavmfcc,indent=4)
    with open(ideafile,'w') as f:
        f.write(json_str)
    ##单独测试一个文件
    #wavmfcc={}
    #wavpath='E:/FFOutput/B/SYJ.2.BTY.wav'
    #y,sr = librosa.load(wavpath)
    #mfcc = librosa.feature.mfcc( y,sr,n_mfcc=20 )
    #wavmfcc[wavpath]=mfcc.tolist()
    #print(wavmfcc)
    pass