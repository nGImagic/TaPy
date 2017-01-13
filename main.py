#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:42:58 2017

@author: harti
"""

from functions import read_data

path_ob = '/Users/harti/switchdrive/nGI_reduction_software/data/data_OB'
path_im = '/Users/harti/switchdrive/nGI_reduction_software/data/data_smp'
path_dc = '/Users/harti/switchdrive/nGI_reduction_software/data/DCs'

(im,ob,dc) = read_data(path_im,path_ob,path_dc)