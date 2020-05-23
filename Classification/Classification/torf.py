import audio_anaylsis
import rnn_classifier

k=0.02
y=34864
n=44142
p=0.5
Ec=2000
Eb=1000
Em=1519

def torf(filepath,dp,We,Wl,Wf,d):#参数：文件路径，询问递减率,能量权重，有声段长度权重，频率权重   
    yorn = wav_yorn(filepath,k,y,n,p)
    times=0
    while times<4 and yorn<1:
        yorn=wav_yorn(filepath,k,y,n,p)
        times=times+1
    if yorn>1:#多次判断为是则继续往下进行
        x,L,E=get_x(filepath)
        if corb(filepath)>0:#判断为面朝  
            E=E*(Eb+Ec)/2/Ec
        else : #判断为背朝
            E=E*(Eb+Ec)/2/Eb
        Fm,F=get_features(filepath)
        outcome=(We*E/Em+Wl*L/len(x[filepath])*Wf*F/Fm)
        if outcome>d:
            return 1#大于给定清新度值标记为清醒
        else :
            return outcome
    else :#多次判断为否则直接判定为不清醒程度为0
        return 0
if __name__=='__main__':
    wavdir='E:/FFOutput/sound1/'
