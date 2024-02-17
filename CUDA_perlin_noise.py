# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:54:01 2024

@author: 29150
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 19:20:13 2023

@author: 29150

非连续柏林噪声，采用哈希散列
"""


import numpy as np
import torch
from PIL import Image
import time
import sys
import math




    
    
    
    
def hash32(X,Y,F,SEED):
    '''这里使用纯哈希32函数取得顶点向量'''
    X=X+1
    Y=Y+1
    X=X * 127.1 + Y * 311.7 + F * 101.12
    Y=X * 269.5 + Y * 183.3 + F * 101.12
    SINX=torch.sin(X) * (43758.5453123+SEED/1000)
    SINY=torch.sin(Y) * (43758.5453123+SEED/1000)
    X=(SINX-torch.floor(SINX)) * 2 -1
    Y=(SINY-torch.floor(SINY)) * 2 -1
    
    length = torch.sqrt(X*X+Y*Y)#归一化
    X/=length
    Y/=length
    
    return torch.stack((X,Y),dim=-1)

def noise(shape=(16,16),
          frequency=(8,8),
          continuity=False,
          interpolant=lambda t:t*t*t*(t*(t*6 - 15) + 10),
          seed=1000):
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    cell_size=(shape[0] // frequency[0] , shape[1] // frequency[1])
    pixel_step=(frequency[0] / shape[0] , frequency[1] / shape[1])#每个像素在cell中的相对坐标的单位长度，如cell边长4像素则单位长度0.25
    
    x_coordinates=torch.arange(pixel_step[0]/2, frequency[0], pixel_step[0])#x轴各像素坐标，单位长度1是cell的x轴边长
    y_coordinates=torch.arange(pixel_step[1]/2, frequency[1], pixel_step[1])#y轴各像素坐标
    coordinates=(torch.stack(torch.meshgrid(x_coordinates, y_coordinates), dim = -1) % 1).to(device)#所有像素的坐标，dim=-1保证张量中每点的x，y坐标成对组合好
    
    
    x_anchor,y_anchor=torch.meshgrid(torch.arange(0,frequency[0]+1),torch.arange(0,frequency[1]+1))#获取顶点的坐标
    gradients=hash32(x_anchor,y_anchor,(frequency[0]+frequency[1])/2,seed).to(device)#各顶点的梯度
    
    
    if continuity:
        gradients[:,-1]=gradients[:,0]#最后一列的值设置为第一列的值
        gradients[-1,:]=gradients[0,:]#最后一行的值设置为第一行的值
        
    
    choose_vertex=lambda slice1, slice2: gradients[slice1[0]:slice1[1], slice2[0]:slice2[1]].repeat_interleave(cell_size[0], 0).repeat_interleave(cell_size[1], 1)
    #截取并重复（数目翻倍）所需要的梯度（如cell右上角），由于后面每个cell中有多个像素需要与梯度相乘
    matrix_multiply=lambda expanded_vertex, shift: (torch.stack((coordinates[:,:,0]+shift[0],coordinates[:,:,1]+shift[1]),dim=-1)*expanded_vertex).sum(dim=-1)
    #同时完成顶点指向像素点向量的计算，和梯度与指向向量乘积的运算
    
    n00=matrix_multiply(choose_vertex([0,-1],[0,-1]),[0,0])#图片尺寸，每个像素点的左上角点乘值
    n01=matrix_multiply(choose_vertex([0,-1],[1,None]),[0,-1])
    n10=matrix_multiply(choose_vertex([1,None],[0,-1]),[-1,0])
    n11=matrix_multiply(choose_vertex([1,None],[1,None]),[-1,-1])
    inter_weight=interpolant(coordinates)#获得权重矩阵用于lerp函数（lerp函数泰酷辣）
    
    canva=torch.lerp(torch.lerp(n00, n10, inter_weight[:,:, 0]), torch.lerp(n01, n11, inter_weight[:,:, 0]), inter_weight[:,:, 1])
    
    return (np.array(((canva-float(canva.min()))/(float(canva.max())-float(canva.min()))*255).cpu())).astype(int)


def Stacked_noise(shape=(16,16),
          frequency=(8,8),
          continuity=False,
          stack=1,
          seed=1000):
    canva=np.zeros(shape)
    mutiple=1
    weight=1
    total_weight=0
    for i in range(stack):
        canva=canva+noise(shape,(mutiple*frequency[0],mutiple*frequency[1]),seed=seed)*weight
        total_weight+=weight
        mutiple*=2
        weight/=2
    return canva/total_weight

def falloff(canva,islandSIZE=0.1):#适用于方图
    SIZE=canva.shape[0] if canva.shape[0]<canva.shape[1] else canva.shape[1]
    i_shift=int(math.floor((canva.shape[0]-canva.shape[1])/2)) if canva.shape[0]>canva.shape[1] else 0
    j_shift=int(math.floor((canva.shape[1]-canva.shape[0])/2)) if canva.shape[0]<canva.shape[1] else 0
    for i in range(0,canva.shape[0]):
        for j in range(0,canva.shape[1]):
            if i>i_shift and i<i_shift+SIZE and j>j_shift and j<j_shift+SIZE:
                gradient=1
                gradient/=((i-i_shift)*(j-j_shift))/(SIZE*SIZE)*(1-((i-i_shift)/SIZE))*(1-((j-j_shift)/SIZE))
                gradient-=16
                gradient/=islandSIZE
                canva[i][j]-=gradient
                if canva[i][j]<0: 
                    canva[i][j]=0
            else :
                canva[i][j]=0
    return canva

start_time=time.time()

a=Stacked_noise((512,1024),(8,8),stack=4,seed=2400)
#a=falloff(a)
a=(Image.fromarray(a)).convert('L')
a.save('./gray/'+str(time.strftime('%Y_%m_%d_%H%M%S', time.localtime()))+'.bmp',quality=95)
a.show()

end_time=time.time()

print("生成耗时",end_time-start_time)