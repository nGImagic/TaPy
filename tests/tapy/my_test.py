
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer


class TestClass(unittest.TestCase):
    
    def setUp(self):    
        pass
        
    def test_bad_file_name_raise_ioerror(self):
        """assert error is raised when wrong input data file name is given"""
        _bad_file_name = 'file.fits'
        o_grating = GratingInterferometer()
        self.assertRaises(OSError, o_grating.load, _bad_file_name)
        
    def test_empty_file_name_raise_ioerror(self):
        '''assert error is raised when no input data is given'''
        o_grating = GratingInterferometer()
        self.assertRaises(OSError, o_grating.load)
        