#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:42:58 2017

@author: harti
"""

from functions import read_data,roi

path_ob = '/Users/harti/switchdrive/repos/nGI_magic/r/data/data_OB'
path_im = '/Users/harti/switchdrive/repos/nGI_magic/r/data/data_smp'
path_dc = '/Users/harti/switchdrive/repos/nGI_magic/r/data/DCs'

(im,ob) = read_data(path_im,path_ob,path_dc)
roi(im[0],15,25,40,40,True)