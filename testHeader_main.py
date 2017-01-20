#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:13:09 2017

@author: valsecchi
"""
import os
from PIL import Image
import numpy as np
from astropy.io import fits 
import fitsio
import h5py

def readRead(ii,dc=1):
    """
    readRead()
    it loads images from list of absolute paths and subtract the dark current
    piu
    """
    im_a1 = []       
    for i in ii:
        if i.lower().endswith('.fits'):
            try:         
                im_a1.append(fits.open(i)[0].data)
            except OSError:
                im_a1.append(fitsio.read(i))
        elif i.lower().endswith(('.tiff','.tif')) :
            im_a1.append(np.asarray(Image.open(i)))
        elif i.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
            hdf = h5py.File(i,'r')['entry']['data']['data'].value
            for iScan in hdf:
                im_a1.append(iScan)
        else:
    ##        if you don't want to break the program just comment the raise and eventually uncomment the print for having a feedback
    #        print(os.path.splitext(i)[-1],'file extension not yet implemented....Do it your own way!')
            raise OSError('file extension not yet implemented....Do it your own way!')     
        if dc:
            im_a1 = np.asarray(im_a1)-dc
        else:
            im_a1 = np.asarray(im_a1)
    return im_a1

# Function to read the data and return it as 3D arrays
def read_data(path_im,path_ob,path_dc):
    """
    read()
    """
    return

    return(stack_im_ar,stack_ob_ar)
    
path_ob = 'data/data_OB'
path_im = 'data/data_smp'
path_dc = 'data/DCs'

