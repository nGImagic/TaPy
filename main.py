#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:42:58 2017

@author: harti and valsecchi
"""
from functions import read_data,cropped,createIm,normalization,saveIm,binning,oscillation,createIm_fft
from pixelwiseDPC import pixelWiseDPC,pixelWisePC
import numpy as np


#path_ob = 'data/data_OB'
#path_im = 'data/data_smp'
#path_dc = ''#'data/DCs'

path_ob = 'data/data_OB'
path_im = 'data/data_smp'
path_dc = ''#'data/DCs'

path_dc = ''#'data/DCs'
bin_fac = None                 # no binning either 1 or None, 2x2 binning: bin_fac = 2
norm_param = [3,5,20,40]
crop_param = [10,15,80,60]
oscillationParam = [30,1,1,1]

im,ob = read_data(path_im,path_ob,path_dc)
#im,ob=normalization(im,ob,*norm_param)
#crop_param = [170,170,600,600]
oscillation(im,ob,*oscillationParam,repeatedPeriod=True)
#im,ob = cropped(im,ob,*crop_param)
#im,ob=normalization(im,ob,*norm_param)
#im, ob = binning(im,ob,bin_fac)
#im, ob = win_filt_z(im,ob)
ti, dpci, dfi, vis_map = createIm(im,ob)
#ti, dpci, dfi, vis_map = createIm_fft(im,ob)
oscillation(im,ob,5,5,2,2)
saveIm(ti, dpci, dfi, vis_map,name='name',folder='folder',overWrite=True)


