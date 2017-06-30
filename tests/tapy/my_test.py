
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer


class TestClass(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../../data/'))
        
    def test_bad_file_name_raise_ioerror(self):
        """assert error is raised when wrong input data file name is given"""
        _bad_file_name = 'file.fits'
        o_grating = GratingInterferometer()
        self.assertRaises(OSError, o_grating.load, _bad_file_name)
        
    def test_empty_file_name_raise_ioerror(self):
        '''assert error is raised when no input data is given'''
        o_grating = GratingInterferometer()
        self.assertRaises(OSError, o_grating.load)
        
    def test_loading_correct_fits(self):
        '''assert fits file is correctd loaded'''
        fits_file = self.data_path + '/fits/image001.fits'
        o_grating = GratingInterferometer()
        o_grating.load(file_name=fits_file)
        data = o_grating.data
        [height, width] = np.shape(data)
        self.assertEqual(np.shape(data), (5, 5))
        expected_data = np.ones([5,5])
        for col in np.arange(5):
            expected_data[:,col] = col        
        self.assertTrue((data == expected_data).all())

    