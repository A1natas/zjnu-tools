#utf-8
from numpy import *
from matplotlib import pyplot as plt
from sys import argv
from time import strftime,localtime,sleep
import os
import threading


imgsave_mutex = threading.Lock()
def img_encode(keys,inputpath,level,moreSafe_X,moreSafe_Y,delete_source,outfile=''):
    #? 加密过程
    keys = list(map(ord,keys))
    keylen = len(keys)
    image = plt.imread(inputpath)
    image = array(plt.imread(inputpath))

    if moreSafe_X:
        groups_X = int(len(image)/level)
        
        #? 获取行像素的加密流
        S = []
        T = []
        for i in range(groups_X):
            S.append(i)
            T.append(keys[i % keylen])
        j = 0
        for i in range(groups_X):
            j = (j+S[i]+T[i])%groups_X
            S[i],S[j] = S[j],S[i]
        if groups_X%2 == 1:
            S = S[:-1]
        stream_X = array(S).reshape(2,int(len(S)/2))
        stream_X *= level
        group1 = []
        group2 = []
        for i in range(len(stream_X[0])):
            group1.append(stream_X[0][i])
            group2.append(stream_X[1][i])
            for j in range(1,level):
                group1.append(stream_X[0][i] + j)
                group2.append(stream_X[1][i] + j)
        
        #? 根据行像素加密流，行行交换
        image[group1+group2,:,:] = image[group2+group1,:,:]

    if moreSafe_Y:
        groups_Y = int(len(image[0])/level)
        #? 获取列像素的加密流
        S = []
        T = []
        for i in range(groups_Y):
            S.append(i)
            T.append(keys[i % keylen])
        j = 0
        for i in range(groups_Y):
            j = (j+S[i]+T[i])%groups_Y
            S[i],S[j] = S[j],S[i]
        if groups_Y%2 == 1:
            S = S[:-1]
        stream_Y = array(S).reshape(2,int(len(S)/2))
        stream_Y *= level
        group1 = []
        group2 = []
        for i in range(len(stream_Y[0])):
            group1.append(stream_Y[0][i])
            group2.append(stream_Y[1][i])
            for j in range(1,level):
                group1.append(stream_Y[0][i] + j)
                group2.append(stream_Y[1][i] + j)
        #? 根据列像素加密流，列列交换
        image[:,group1+group2,:] = image[:,group2+group1,:]

    #? 输出目录为当前时间
    outpath = strftime("%Y%m%d%H%M%S", localtime())
    outpath+='.png'
    outpath = os.path.join(os.path.dirname(inputpath),outpath)
    
    if outfile:
        if delete_source:
            os.remove(inputpath)
        plt.imsave(outfile,image)
    else:
        #? 防止输出文件名一样导致色图丢失，加了线程锁和如果有相同文件名就等待0.5秒
        imgsave_mutex.acquire()
        while os.path.exists(outpath):
            outpath = strftime("%Y%m%d%H%M%S", localtime())
            outpath+='.png'
            outpath = os.path.join(os.path.dirname(inputpath),outpath)
            sleep(0.5)
        plt.imsave(outpath,image)
        if delete_source:
            os.remove(inputpath)
        print('succeed: ' + inputpath)
        imgsave_mutex.release()

if __name__ == '__main__':
    args = list(argv)
    img_types = ['jpg','png','gif']
    if len(args) <= 1 or "-help" in args:
        help_msg = '''
==================================
||                              ||
||   欢迎使用杰哥色图加密脚本!  ||
||                              ||
==================================
可控参数：
    -k 设置秘钥(默认114514)
    -o 设置输出文件名(不支持批量加密)
    -l 设置加密强度[1-x](默认40,数字越小加密越强，最大不超过min(横向分辨率,纵向分辨率))
    -d 删除原图
    -x-only 只交换行像素
    -y-only 只交换纵像素'''
        print(help_msg.strip())
        exit()
    key = "114514"
    outfile = ""
    level = 40
    moreSecure_X = True
    moreSecure_Y = True
    delete_source = False
    skip = False
    for i in range(len(args)):
        if skip:
            skip = False
            continue
        if args[i][0] == '-':
            if args[i][1] == 'k':
                key = args[i+1]
                skip = True
            elif args[i][1] == 'o':
                outfile = args[i+1]
                skip = True
            elif args[i][1] == 'l':
                level = int(args[i+1])
                skip = True
            elif args[i][1] == 'd':
                delete_source = True
            elif 'only' in args[i]:
                if args[i][1] == 'x':
                    moreSecure_X = True
                    moreSecure_Y = False
                elif args[i][1] == 'y':
                    moreSecure_X = False
                    moreSecure_Y = True
        else:
            input_path = args[i]

    if os.path.isdir(input_path):
        threads = []
        filepath = []
        #? 遍历目标目录 给每个图片文件创建一个子线程
        for root,dirs,files in os.walk(input_path):
            for file in files:
                path = os.path.join(root,file)
                if path[-3:] in img_types:
                    #?把所有图片文件路径保存在数组中
                    filepath.append(path)
        #? 创建线程
        for path in filepath:       
            now_thread = threading.Thread(target=img_encode,args=(key,path,level,moreSecure_X,moreSecure_Y,delete_source))   
            threads.append(now_thread)
            now_thread.start()
        for thread in threads:
            thread.join()
    else:
        print(outfile)
        img_encode(key,input_path,level,moreSecure_X,moreSecure_Y,delete_source,outfile)
