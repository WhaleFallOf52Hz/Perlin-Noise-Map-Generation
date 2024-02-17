# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 21:52:20 2024

@author: 29150
"""

import numpy as np
from PIL import Image
import math
import sys
import time
import multiprocessing


def Bresenham(Theta_input,upper):
    result=[]
    result.append([0,0])
    if Theta_input>=180:
        Theta_input-=180
    if Theta_input==0 or Theta_input==90 :
        raise Exception("角度错误")
        
        
    if Theta_input==45:
        for i in range(1,upper):
            result.append([i,i])
    elif Theta_input==135:
        for i in range(1,upper):
            result.append([-i,i])
    else:
        if Theta_input>0 and Theta_input<45:
            Theta=Theta_input/180*math.pi
        elif Theta_input>45 and Theta_input<90:
            Theta=(90-Theta_input)/180*math.pi
        elif Theta_input>90 and Theta_input<135:
            Theta=(Theta_input-90)/180*math.pi
        elif Theta_input>135 and Theta_input<180:
            Theta=(180-Theta_input)/180*math.pi
        k=math.tan(Theta)
        xi=0
        yi=0
        ei=2*k-1
        for i in range(1,upper):
            xi+=1
            if ei>=0:
                ei=ei-2+2*k
                yi+=1
            else:
                ei=ei+2*k
            
            if Theta_input>0 and Theta_input<45:
                result.append([xi,yi])
            elif Theta_input>45 and Theta_input<90:
                result.append([yi,xi])
            elif Theta_input>90 and Theta_input<135:
                result.append([-yi,xi])
            elif Theta_input>135 and Theta_input<180:
                result.append([xi,-yi])
    return result

def block_judge(canva,Theta_input,Phi_input,long_shade=1):
    SIZE=(canva.shape[0])
    X=canva.shape[0]
    Y=canva.shape[1]
    isblocked=[]#阴影高度、是否遮盖
    for i in range(0,X):
        c=[]
        for j in range(0,Y):
            c.append([canva[i][j] if canva[i][j]>30 else 0,False])
        isblocked.append(c)
    
    Theta=math.pi*(Theta_input/180)    #0到2pi 极轴由中心指向下方（南方）
    Phi=math.pi*(Phi_input/180) #0到pi/2

    ct=math.cos(Theta)
    st=math.sin(Theta)
    tp=math.tan(Phi)/long_shade
    if Theta_input==0:
        for i in range(X-2,-1,-1):
            for j in range(0,Y):
                if isblocked[i+1][j][0]-1*tp>isblocked[i][j][0]:
                    isblocked[i][j][0]=isblocked[i+1][j][0]-1*tp
                    isblocked[i][j][1]=True
    elif Theta_input==90:
        for j in range(Y-2,-1,-1):
            for i in range(0,X):
                if isblocked[i][j+1][0]-tp>isblocked[i][j][0]:
                    isblocked[i][j][0]=isblocked[i][j+1][0]-tp
                    isblocked[i][j][1]=True

    elif Theta_input==180:
        for i in range(1,X):
            for j in range(0,Y):
                if isblocked[i-1][j][0]-tp>isblocked[i][j][0]:
                    isblocked[i][j][0]=isblocked[i-1][j][0]-tp
                    isblocked[i][j][1]=True

        
            
    elif Theta_input==270:
        for j in range(1,Y):
            for i in range(0,X):
                if isblocked[i][j-1][0]-tp>isblocked[i][j][0]:
                    isblocked[i][j][0]=isblocked[i][j-1][0]-tp
                    isblocked[i][j][1]=True




    elif Theta_input>0 and Theta_input<=45:
        ll=Bresenham(Theta_input, X)
        fall=ll[len(ll)-1][1]
        for i in range(0,len(ll)):
            ll[i][1]=ll[i][1]-fall

        for j in range(0,fall+Y):
            for i in range(X-2,-1,-1):
                if ll[i+1][1]+j>Y-1 or ll[i][1]+j<0 :continue
                if isblocked[i][ll[i][1]+j][0]<isblocked[i+1][ll[i+1][1]+j][0]-tp*(1/ct):
                    isblocked[i][ll[i][1]+j][0]=isblocked[i+1][ll[i+1][1]+j][0]-tp*(1/ct)
                    isblocked[i][ll[i][1]+j][1]=True
    elif Theta_input>180 and Theta_input<225:
        ll=Bresenham(Theta_input, X)
        fall=ll[len(ll)-1][1]
        for i in range(0,len(ll)):
            ll[i][1]=ll[i][1]-fall
        for j in range(0,fall+Y):
            for i in range(1,X):
                if ll[i][1]+j>Y-1 or ll[i-1][1]+j<0 :continue
                if isblocked[i][ll[i][1]+j][0]<isblocked[i-1][ll[i-1][1]+j][0]+tp*(1/ct):
                    isblocked[i][ll[i][1]+j][0]=isblocked[i-1][ll[i-1][1]+j][0]+tp*(1/ct)
                    isblocked[i][ll[i][1]+j][1]=True
    elif Theta_input>45 and Theta_input<90:
        ll=Bresenham(Theta_input, Y)
        fall=ll[len(ll)-1][0]
        for i in range(0,len(ll)):
            ll[i][0]=ll[i][0]-fall
            
        for i in range(0,fall+X):
            for j in range(Y-2,-1,-1):
                if ll[j+1][0]+i>X-1 or ll[j][0]+i<0 :continue
                if isblocked[ll[j][0]+i][j][0]<isblocked[ll[j+1][0]+i][j+1][0]-tp*(1/st):
                    isblocked[ll[j][0]+i][j][0]=isblocked[ll[j+1][0]+i][j+1][0]-tp*(1/st)
                    isblocked[ll[j][0]+i][j][1]=True
    elif Theta_input>225 and Theta_input<270:
        ll=Bresenham(Theta_input, Y)
        fall=ll[len(ll)-1][0]
        for i in range(0,len(ll)):
            ll[i][0]=ll[i][0]-fall
            
        for i in range(0,fall+X):
            for j in range(1,Y-1):
                if ll[j][0]+i>X-1 or ll[j-1][0]+i<0 :continue
                if isblocked[ll[j][0]+i][j][0]<isblocked[ll[j-1][0]+i][j-1][0]+tp*(1/st):
                    isblocked[ll[j][0]+i][j][0]=isblocked[ll[j-1][0]+i][j-1][0]+tp*(1/st)
                    isblocked[ll[j][0]+i][j][1]=True
    elif Theta_input>90 and Theta_input<=135:
        ll=Bresenham(Theta_input, Y)
        fall=-ll[len(ll)-1][0]
        for i in range(0,fall+X):
            for j in range(Y-2,-1,-1):
                if ll[j+1][0]+i<0 or ll[j][0]+i>X-1 :continue
                if isblocked[ll[j][0]+i][j][0]<isblocked[ll[j+1][0]+i][j+1][0]-tp*(1/st):
                    isblocked[ll[j][0]+i][j][0]=isblocked[ll[j+1][0]+i][j+1][0]-tp*(1/st)
                    isblocked[ll[j][0]+i][j][1]=True
    elif Theta_input>270 and Theta_input<=315:
        ll=Bresenham(Theta_input, Y)
        fall=-ll[len(ll)-1][0]
        for i in range(0,fall+X):
            for j in range(1,Y):
                if ll[j][0]+i<0 or ll[j-1][0]+i>X-1 :continue
                if isblocked[ll[j][0]+i][j][0]<isblocked[ll[j-1][0]+i][j-1][0]+tp*(1/st):
                    isblocked[ll[j][0]+i][j][0]=isblocked[ll[j-1][0]+i][j-1][0]+tp*(1/st)
                    isblocked[ll[j][0]+i][j][1]=True
    elif Theta_input>135 and Theta_input<180:
        ll=Bresenham(Theta_input, X)
        fall=-ll[len(ll)-1][1]

        for j in range(0,fall+Y):
            for i in range(1,X):
                if ll[i-1][1]+j>Y-1 or ll[i][1]+j<0 :continue
                if isblocked[i][ll[i][1]+j][0]<isblocked[i-1][ll[i-1][1]+j][0]+tp*(1/ct):
                    isblocked[i][ll[i][1]+j][0]=isblocked[i-1][ll[i-1][1]+j][0]+tp*(1/ct)
                    isblocked[i][ll[i][1]+j][1]=True
    elif Theta_input>315 and Theta_input<360:
        ll=Bresenham(Theta_input, X)
        fall=-ll[len(ll)-1][1]

        for j in range(0,fall+Y):
            for i in range(X-2,-1,-1):
                if ll[i][1]+j>Y-1 or ll[i+1][1]+j<0 :continue
                if isblocked[i][ll[i][1]+j][0]<isblocked[i+1][ll[i+1][1]+j][0]-tp*(1/ct):
                    isblocked[i][ll[i][1]+j][0]=isblocked[i+1][ll[i+1][1]+j][0]-tp*(1/ct)
                    isblocked[i][ll[i][1]+j][1]=True
    
    
    return isblocked

def enColor(canva,shaded=False,Theta_input=180,Phi_input=60,long_shade=1):
    if Theta_input>=360 or Theta_input<0:
        raise Exception ("Theta out of range")
    if Phi_input>90 or Phi_input<0::
        raise Exception ("Phi out of range")
    if shaded==True:
        isblocked=block_judge(canva,Theta_input,Phi_input,long_shade=long_shade)
    X=canva.shape[0]
    Y=canva.shape[1]
    newcanva=Image.new('RGB',(Y,X))
    for i in range(0,X):
        for j in range(0,Y):
        #if i<10:
        #    newcanva.putpixel((i,j), (int(0),int(0),int(0)))
        #    continue
        #print(i,' ',j)
            a=1
            if shaded==True and isblocked[i][j][1] :
                a=0.5
            if canva[i][j]<=15:
                newcanva.putpixel((j,i), (int(99*a),int(164*a),int(167*a)))#由于array坐标位置和putpixel位置相逆
            elif canva[i][j]>15 and canva[i][j]<=30:
                newcanva.putpixel((j,i), (int(158*a),int(187*a),int(188*a)))
            elif canva[i][j]>30 and canva[i][j]<=60:
                newcanva.putpixel((j,i), (int(213*a),int(181*a),int(157*a)))
            elif canva[i][j]>60 and canva[i][j]<=106:
                newcanva.putpixel((j,i), (int(151*a),int(172*a),int(92*a)))
            elif canva[i][j]>106 and canva[i][j]<=156:
                newcanva.putpixel((j,i), (int(101*a),int(133*a),int(66*a)))
            elif canva[i][j]>156 and canva[i][j]<=206:
                newcanva.putpixel((j,i), (int(71*a),int(117*a),int(70*a)))
            elif canva[i][j]>206 and canva[i][j]<=255:
                newcanva.putpixel((j,i), (int(109*a),int(117*a),int(133*a)))
    return newcanva
name='2024_02_15_185432'
canva=np.array(Image.open('./gray/'+name+'.bmp'))

start_time=time.time()

Theta_input=170#度数表示,0度光源在正下方，逆时针增大角度
Phi_input=60#度数表示

sealevel=30
newcanva=enColor(canva,True,Theta_input,Phi_input,long_shade=3)

end_time=time.time()

newcanva.show()
newcanva.save('./color/'+name+'_Theta'+str(Theta_input)+'_Phi'+str(Phi_input)+'.bmp')
print("上色耗时",end_time-start_time)
