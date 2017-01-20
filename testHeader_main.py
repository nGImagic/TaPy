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
from pathlib import Path

def readRead(path,dc=1):
    """
    readRead()
    
    """
    my_file = Path(path)
    if my_file.is_file():
        im_a1 = []
        if path.lower().endswith('.fits'):
            try:         
                im_a1.append(fits.open(path)[0].data)
            except OSError:
                im_a1.append(fitsio.read(path))
        elif path.lower().endswith(('.tiff','.tif')) :
            im_a1.append(np.asarray(Image.open(path)))
        elif path.lower().endswith(('.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5')): 
            hdf = h5py.File(path,'r')['entry']['data']['data'].value
            for iScan in hdf:
                im_a1.append(iScan)
        else:
    ##        if you don't want to break the program just comment the raise and eventually uncomment the print for having a feedback
    #        print(os.path.splitext(path)[-1],'file extension not yet implemented....Do it your own way!')
            raise OSError('file extension not yet implemented....Do it your own way!')     
        if dc:
            im_a1 = np.asarray(im_a1)-dc
        else:
            im_a1 = np.asarray(im_a1)
        return im_a1
    else:
        print(path,'does not exist')


# Function to read the data and return it as 3D arrays
def read_data(path_im,path_ob,path_dc):
    """
    read()
    """
    if path_dc:
        # Load DCs and average them
        filenames_dc = [name for name in os.listdir(path_dc) if name.lower().endswith(('.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5'))]
        filenames_dc.sort()
        im_a1 = []
        for name in filenames_dc:
            full_path_name = path_dc+'/'+name
            print(full_path_name)
            im_a1.append(readRead(full_path_name))
        im_a1 = np.asarray(im_a1)
        im_a1 = np.sum(im_a1,axis=0)/np.shape(im_a1)[0]
    return im_a1
path_ob = 'data/data_OB'
path_im = 'data/data_smp'
path_dc = 'data/DCs'


io = read_data(0,0,'data/data_smp')
