import os

def StaticLengthNumber(str_number,length):#函数主要将二进制数转为编码字符串
    str_number = str(str_number)
    while(len(str_number) < length):
        str_number = '0' + str_number
    return str_number

def get_mark(filename):
     code = ""
     mark = ["BFN","BFY","BTN","BTY","CFN","CFY","CTN","CTY"]          
     #C1B0 F0T1 N0Y1
     #唯一编码，分别从‘000’按序递增到‘111’
     #d.1.BTN.wav,  010=y[0] y[0]的type 是str, if y[0][1]='1' : 代表T     int(y[i][2])>0 代表yes    else 代表不是N
     for j in mark:
            if j in filename:
                b = bin(mark.index(j)).replace('0b','')
                code = StaticLengthNumber(b,3)
                break
     return code

def get_y(filepath):
    filename = os.listdir(filepath) 
    y = {}
    #存放标记数据的数组
    ty = [] #存放临时y的数组
    corb=[]
    torf=[]
    yorn=[]
    for i in filename:
        i.upper()                        #将所有文件名转为大写
        y[i] = get_mark(i)
        print(i,",",y[i])
    #将字典中的value全部取出来，转换为整型放在列表中
    #ty = list(y.values())
    ty = list(map(str,y.values()))
    #将标签标记的3个参数分离,分别存入不同数组
    for i in ty:
        i=int(i)
        if i>=100:
            corb.append(1)
            i=i%10
        elif i<100:
            corb.append(0)
        if i>=10:
            torf.append(1)
            i=i%10
        elif i<10:
            torf.append(0)
        if i==1:
            yorn.append(1)
        elif i==0:
            yorn.append(0)


    return y,ty,corb,torf,yorn

if __name__ == '__main__':
    #filepath = "C:/Users/1/Documents/Dev/Waking/Classification/Classification/data/FFOutput/" 
    code = get_mark('d.1.BTN.wav')
    print(code)
    print(code[0],code[1],code[2])
    #y,ty,corb,torf,yorn = get_y(filepath)
    #测试输出
    #print(y)
    #print(ty)
    #print(type(ty))
    #print("corb:",corb)
    #print("torf:",torf)
    #print("yorn:",yorn)
    