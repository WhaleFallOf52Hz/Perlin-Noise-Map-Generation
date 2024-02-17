_个人小练习——基于柏林噪声的地形生成_

## 概述
这是一个基于柏林噪声的试验性程序，用于二维平面上高度图地形的生成。在[https://www.bilibili.com/video/BV16C4y1S7Rh/]() 启发下完成，包含了地形生成（可选岛屿化）与地形上色（可选平行光阴影）两部分。
## CUDA_perlin_noise.py
此程序是在个人源程序的基础上，参考[https://github.com/pvigier/perlin-numpy/blob/master/perlin_numpy/perlin2d.py]() ，利用pytorch矩阵计算加速生成的产物：
* `noise( )` 是基础的柏林噪声程序，根据输入所要求的尺寸、频率、是否连续、随机种子生成的单频率柏林噪声
* `Stacked_noise( )` 通过调用`noise()`，输出多重倍频叠加的柏林噪声
* `falloff( )` 则将输入的柏林噪声(array格式)根据特定函数转化为岛屿形
## color.py
此程序通过Bresenham直线算法，计算光线与阴影，达到为图片上色的目的，**暂未实现并行化**
## 示例
![image1](/sample_images/256x256image_Theta180_Phi60.bmp "256x256,Theta（方位角）=180,Phi（高度角）=60")



---

_Personal Exercise - Terrain Generation Based on Berlin Noise_
## Overview
This is an experimental program based on Berlin noise for generating altitude maps on a 2d plane, inspired by [https://www.youtube.com/watch?v=bMTeCqNkId8]() .It includes two parts: terrain generation (optional islanding) and terrain coloring (optional shadows by directional light).
## CUDA_perlin_noise.py
This program is based on the personal source code, with reference to [https://github.com/pvigier/perlin-numpy/blob/master/perlin_numpy/perlin2d.py]() . It now can accelerate computing with pytorch matrix (CUDA).
* `noise()` is a basic Berlin noise program that generates single frequency Berlin noise following the required size, frequency, continuity, and random seed of the input
* `Stacked_noise( )` utilizes `noise()` to output stacked Berlin noise with multiple frequency
* `falloff( )` transform the input noise into a island-shape one
## color.py
Color the noise(or so called _height map_). Make it into a real height map with shadow. It's based on Bresenham's line algorithm.
