
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer
from tapy.roi import ROI


class TestLoadingNormalization(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
    
    #def test_cropping_raises_error_when_no_data_loaded(self):
        #'''assert error raised when no data loaded'''
        #o_grating = GratingInterferometer()
        #self.assertRaises(IOError, o_grating.crop)