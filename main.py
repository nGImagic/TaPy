#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:42:58 2017

@author: harti and valsecchi
"""
from functions import read_data,cropped,createIm,normalization,saveIm,binning,oscillation,createIm_fft,med_filt_z
from pixelwiseDPC import pixelWiseDPC,pixelWisePC

path_ob = 'data/phase/data_OB'
path_im = 'data/phase/data_smp'
path_dc = ''#'data/DCs'

norm_param = [3,5,20,40]
crop_param = [10,15,80,60]
bin_fac = None                 # no binning either 1 or None, 2x2 binning: bin_fac = 2

(im,ob) = read_data(path_im,path_ob,path_dc)
#im,ob=normalization(im,ob,*norm_param)
#im,ob = cropped(im,ob,*crop_param)
#im, ob = binning(im,ob,bin_fac)
#im, ob = med_filt_z(im,ob,3)
ti, dpci, dfi, vis_map = createIm(im,ob)
#ti, dpci, dfi, vis_map = createIm_fft(im,ob)
saveIm(ti, dpci, dfi, vis_map,name='name',folder='med_filt',overWrite=True)



