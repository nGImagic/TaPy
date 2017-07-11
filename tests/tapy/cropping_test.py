
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer
from tapy.roi import ROI


class TestCropping(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
    
    def test_cropping_raises_error_when_no_data_and_ob_loaded(self):
        '''assert error raised when no sample and ob data loaded'''
        o_grating = GratingInterferometer()
        _roi = ROI(x0=0, y0=0, x1=4, y1=4)
        self.assertRaises(IOError, o_grating.crop, roi=_roi)
        
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample'
        o_grating.load(folder=sample_path)
        self.assertRaises(IOError, o_grating.crop, roi=_roi)
        
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob'
        o_grating.load(folder=ob_path, data_type='ob')
        self.assertRaises(IOError, o_grating.crop, roi=_roi)
        
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob'
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.normalization()
        self.assertTrue(o_grating.crop(roi=_roi))
        
        