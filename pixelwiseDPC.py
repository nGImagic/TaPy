#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:13:09 2017

@author: harti and valsecchi
"""
import scipy

def pixelWiseDPC(dpci,p2um=4,d1cm=1.94,lambdaAmstr=4.1):
    """
    formula:
        d Φ / d x  =       (p2 / λ * d1) φ           
    according to SI 
    """
    
    dphi_over_dxPixel = (p2um*1e-6)/(lambdaAmstr*1e-10*d1cm*1e-2)*dpci
    scipy.integrate.simps()
    return dphi_over_dxPixel
