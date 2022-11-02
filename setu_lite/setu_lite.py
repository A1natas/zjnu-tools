#utf-8
'''
===============================
||                            ||
||   欢迎使用杰哥色图加密脚本!  ||
||                            ||
===============================
使用说明
只需要在脚本当前目录下输入
python3 脚本文件名 待解密色图路径/文件夹 秘钥 加密程度 是否同时交换行列
例：python3 setulite.py ./1.png 秘钥 [level(int)] [moreSafe(True/False)]
该脚本同样可以用来加密
'''

#---------可供改变参数----------------------
#? level用于调整需要加密的程度，代表交换像素的行/列的最小单位，越大加密程度越低
level = 40
#? moreSafe为True时不仅会交换行像素，还会交换列像素，更安全，但是加密图片会更大。
moreSafe = True
#-----------------------------------------

from numpy import *
from matplotlib import pyplot as plt
from sys import argv
from time import strftime,localtime,sleep
import os
import threading


imgsave_mutex = threading.Lock()
def img_encode(keys,inputpath):
    #? 加密过程
    keys = list(map(ord,keys))
    keylen = len(keys)
    image = plt.imread(inputpath)
    image = array(plt.imread(inputpath))

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

    if moreSafe:
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
    
    #? 防止输出文件名一样导致色图丢失，加了线程锁和如果有相同文件名就等待0.5秒
    imgsave_mutex.acquire()
    while os.path.exists(outpath):
        outpath = strftime("%Y%m%d%H%M%S", localtime())
        outpath+='.png'
        outpath = os.path.join(os.path.dirname(inputpath),outpath)
        sleep(0.5)
    plt.imsave(outpath,image)
    os.remove(inputpath)
    print('succeed: ' + inputpath)
    imgsave_mutex.release()

if __name__ == '__main__':
    args = list(argv)
    img_types = ['jpg','png','gif']
    if len(args) > 4:
        if args[4] == 't':
            moreSafe = True
        elif args[4] == 'f':
            moreSafe = False
    if len(args) > 3:
        level = int(args[3])
    if len(args) > 4:
        moreSafe = bool(args[4])
    if os.path.isdir(args[1]):
        threads = []
        filepath = []
        #? 遍历目标目录 给每个图片文件创建一个子线程
        for root,dirs,files in os.walk(args[1]):
            for file in files:
                path = os.path.join(root,file)
                if path[-3:] in img_types:
                    #?把所有图片文件路径保存在数组中
                    filepath.append(path)
        #? 创建线程
        for path in filepath:       
            now_thread = threading.Thread(target=img_encode,args=(args[2],path))   
            threads.append(now_thread)
            now_thread.start()
        for thread in threads:
            thread.join()
    else:
        img_encode(args[2],args[1])
