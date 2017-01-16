#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:42:58 2017

@author: harti
"""

from functions import read_data,cropped,createIm

path_ob = 'data/data_OB'
path_im = 'data/data_smp'
path_dc = 'data/DCs'

norm_param = [3,5,2,2]
crop_param = [10,15,50,50]


(im,ob) = read_data(path_im,path_ob,path_dc)
#im,ob = normalization(im,ob,*norm_param)
im,ob = cropped(im,ob,*crop_param)

TI, DPCI, DFI = createIm(im,ob)