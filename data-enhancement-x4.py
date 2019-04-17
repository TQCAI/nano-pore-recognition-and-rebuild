'''
数据增强脚本。对数据集中的每个图片旋转90度4次。
这个脚本放置在[数据集文件夹]外面。脚本执行后，形成[数据增强文件夹]
对于[数据集文件夹]，原图为0001.jpg的命名格式(%04d.jpg)，RGB图
                 标注图为0001_gt.jpg的命名格式(%04d_gt.jpg)，灰度图，有孔隙的地方值为255，没有的地方值为0

'''
import os
import numpy as np
import pylab as plt
import cv2
import datetime
import random
from skimage import io

# [数据集文件夹] 名称
input='images'
# [数据增强文件夹] 名称
output='enhancement-x4'



def build_shuffle_list(length):
    '''
    建立一个编号列表。线性递增表为[0,1,...,length-1]，对这个线性递增表进行洗牌，作为输出文件的序号
    :param length:
    :return:
    '''
    lst=np.arange(length)
    np.random.shuffle(lst)
    return lst


def buildDir(name):
    '''对于文件名name，如果不存在则创建'''
    if not os.path.exists(name):
        os.makedirs(name)

def add_log(info):
    '''日志'''
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    with open('log.txt','a+') as f:
        f.writelines(info + str(nowTime) + '\n')


def RotateClockWise90(img):
    '''
    :param img: 输入图
    :return: 对输入图顺时针旋转90度，输出
    '''
    trans_img = cv2.transpose( img )
    new_img = cv2.flip(trans_img, 1)
    return new_img

def saveFiles(img,data,lst):
    # 获取列表的第一项
    pos=lst[0]
    # 删除第一项（维护后续操作的完备性）
    del lst[0]
    # 只取前3个通道(R,G,B)，因为有一个bug导致存在第四个无用的通道。
    img=img[:,:,:3]
    # 保存旋转后的原图和标注图
    io.imsave(f'{output}/{pos:04d}.jpg',img)
    io.imsave(f'{output}/{pos:04d}_gt.jpg', data)


if __name__ == '__main__':
    add_log('开始时间：')
    buildDir(output)
    myFiles=[]  # 文件列表
    for (root, dirs, files) in os.walk(input):
        for file in files:
            # 如果【不是标注图】并且【是jpg格式】
            if file.find("_gt")<0 and file.find('.jpg')>=0:
                myFiles.append(file)   # 添加到文件列表
        break  # os.walk只对当前目录遍历一层
    # 对文件列表进行洗牌
    random.shuffle(myFiles)
    length=len(myFiles)*4  # 因为需要旋转4个角度
    # 建立一个编号列表。线性递增表为[0,1,...,length-1]，对这个线性递增表进行洗牌，作为输出文件的序号
    lst=build_shuffle_list(length)
    lst=list(lst)
    for i,s in enumerate(myFiles):  #i：操作序号，s：当前文件名
        # 分离文件名和扩展名。name为当前文件文件名（无后缀）
        name=os.path.splitext(s)[0]
        print(i,name)
        imgName=f'{input}/'+name+'.jpg'       #输入原图
        dataName=f'{input}/'+name+'_gt.jpg'   #输入标注图
        img=plt.imread(imgName)   #图片读取
        data=plt.imread(dataName)
        # 直接保存
        saveFiles(img,data,lst)
        for j in range(3):  #连续旋转3次
            img=RotateClockWise90(img)
            data=RotateClockWise90(data)
            saveFiles(img, data, lst)
    add_log('结束时间：')
    # 对于长操作，操作后关机
    # os.system('poweroff')

