
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
        o_grating.normalization()
        self.assertTrue(o_grating.crop(roi=_roi))
        
    def test_roi_object_passed_to_crop(self):
        '''assert wrong roi type raises a ValueError'''
        _roi = {'x0':0, 'y0':1}
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob'
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.normalization()
        self.assertRaises(ValueError, o_grating.crop, roi=_roi)
        
    def test_crop_works(self):
        '''assert crop of sample and ob works correctly'''
        x0, y0, x1, y1 = 0, 0, 2, 2
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        o_grating = GratingInterferometer()
        sample_path = self.data_path + '/tif/sample'
        o_grating.load(folder=sample_path)
        ob_path = self.data_path + '/tif/ob'
        o_grating.load(folder=ob_path, data_type='ob')
        o_grating.normalization()
        _expected_sample = o_grating.data['sample']['data'][0]
        _expected_sample = _expected_sample[y0:y1+1, x0:x1+1]
        _expected_ob = o_grating.data['ob']['data'][0]
        _expected_ob = _expected_ob[y0:y1+1, x0:x1+1]
        o_grating.crop(roi=_roi)
        _returned_sample = o_grating.data['sample']['data'][0]
        _returned_ob = o_grating.data['ob']['data'][0]
        self.assertTrue((_expected_sample == _returned_sample).all())
        self.assertTrue((_expected_ob == _returned_ob).all())