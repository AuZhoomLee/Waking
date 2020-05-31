import os

#给出指定目录将文件名存入列表
def get_filename(wavdir):
    pathdir = os.listdir(wavdir)
    filename = []
    for i in pathdir:
        filename.append(os.path.join('%s%s' % (wavdir,i)))
    pass
    #print(filename)
    return filename


  
if __name__ == '__main__':
    wavdir = 'D:/FFOutput/'
    filename = get_filename(wavdir)
    print(type(filename))
    count = 0
    for i in filename:
        count = count + 1
        print(count,i)
