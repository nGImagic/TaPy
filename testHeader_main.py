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
#import fitsio
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
#        if dc:
        im_a1 = np.asarray(im_a1)-dc
#        else:
#            im_a1 = np.asarray(im_a1)
        return im_a1
    else:
        print(path,'does not exist')


# Function to read the data and return it as 3D arrays
def read_data(path_im,path_ob,path_dc):
    """
    read()
    """
#    Dark current
    imExt = ['.fits','.tiff','.tif','.hdf','.h4','.hdf4','.he2','h5','.hdf5','.he5']
    if path_dc:
        im_a1 = []
        filenames_dc = [name for name in os.listdir(path_dc) if name.lower().endswith(tuple(imExt))]
        filenames_dc.sort()
        for name in filenames_dc:
            full_path_name = path_dc+'/'+name
            print(full_path_name)
            im_a1.append(readRead(full_path_name))
        im_a1 = np.asarray(im_a1)
        im_a1 = np.sum(im_a1,axis=0)/np.shape(im_a1)[0]
    
#    Open beam
    filenames_ob = [name for name in os.listdir(path_ob) if name.lower().endswith(tuple(imExt))]
    filenames_ob.sort()
    stack_ob = []
    for name in filenames_ob:
        full_path_name = path_ob+'/'+name
        print(full_path_name)
        if path_dc:
            stack_ob.append(readRead(full_path_name,im_a1)) #with dc
        else:
            stack_ob.append(readRead(full_path_name))   #without dc
    stack_ob = np.asarray(stack_ob)
    
#    Projections
    filenames_im = [name for name in os.listdir(path_im) if name.lower().endswith(tuple(imExt))]
    filenames_im.sort()
    stack_im_ar = []
    for name in filenames_im:
        full_path_name = path_im+'/'+name
        print(full_path_name)
        if path_dc:
            stack_im_ar.append(readRead(full_path_name,im_a1)) #with dc
        else:
            stack_im_ar.append(readRead(full_path_name))   #without dc
    stack_im_ar = np.asarray(stack_im_ar)
    
    if np.shape(stack_im_ar) != np.shape(stack_ob):
            raise ValueError('Data and  open beam have different shapes')
        
    return stack_im_ar,stack_ob,im_a1
path_ob = 'data/data_OB'
path_im = 'data/data_smp'
path_dc = 'data/DCs'


ll,ob,dc = read_data(path_im,path_ob,path_dc)
