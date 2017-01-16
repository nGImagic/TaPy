#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:42:58 2017

@author: harti
"""

from functions import read_data,cropped,normalization

path_ob = 'data/data_OB'
path_im = 'data/data_smp'
path_dc = 'data/DCs'

(im,ob) = read_data(path_im,path_ob,path_dc)
im,ob = cropped(im,ob)