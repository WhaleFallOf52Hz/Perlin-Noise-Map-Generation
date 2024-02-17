# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 10:27:26 2024

@author: 29150
"""

from CUDA_perlin_noise import Stacked_noise,noise, falloff
from color import enColor
from PIL import Image

pic=Stacked_noise((512,512),(4,4),continuity=True,stack=5,seed=1414)
'''Stacked_noise(shape=(16,16),
          frequency=(8,8),
          continuity=False,
          stack=1,
          seed=1000):'''#return np.array

pic=falloff(pic)#make island


pic=enColor(pic,shaded=True,Theta_input=180,Phi_input=60,long_shade=2)
'''enColor(canva,
        shaded=False,
        Theta_input=180,
        Phi_input=60,
        long_shade=1):'''#return PIL.image

pic.show()
