# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 23:26:39 2015

@author: machaneus
"""
import math
        
def normalizeAngleDegrees(angle):
    if angle>=0:
        div = math.floor(angle/180.0)
    else:
        div = math.ceil(angle/180.0)
    
    return angle - div/abs(div)*(int(abs(div)+1)/2)*360.0