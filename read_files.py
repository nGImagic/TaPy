#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:10:52 2017

@author: harti
"""
import pyfits as pf
import os
from PIL import Image
import numpy as np

path_ob = '/Users/harti/switchdrive/nGI_reduction_software/data/data_OB'
path_im = '/Users/harti/switchdrive/nGI_reduction_software/data/data_smp'
path_dc = '/Users/harti/switchdrive/nGI_reduction_software/data/DCs'

filenames_ob = os.listdir(path_ob)
filenames_ob.sort()

stack_ob = list()

for i in filenames_ob:
    f_name = path_ob + '/' + i
    im = Image.open(f_name)
    im_a = np.array(im)
    stack_ob.append(im_a)

stack_ob_ar = np.asarray(stack_ob)


filenames_im = os.listdir(path_im)
filenames_im.sort()

stack_im = list()

for i in filenames_im:
    f_name = path_im + '/' + i
    im = Image.open(f_name)
    im_a = np.array(im)
    stack_im.append(im_a)

stack_im_ar = np.asarray(stack_im)



filenames_dc = os.listdir(path_dc)
filenames_dc.sort()

f_name = path_dc + '/' + filenames_dc[0]
im = Image.open(f_name)
im_a1 = np.array(im)

for i in filenames_dc:
    f_name = path_dc + '/' + i
    im = Image.open(f_name)
    im_a = np.array(im)
    im_a1 = (im_a1 + im_a)/2