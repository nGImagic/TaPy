
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer
from tapy._utilities import get_sorted_list_images


class TestUtilites(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
        
    def test_all_images_names_retrieved_from_file(self):
        '''assert list of images are correctly retrieved from individual file name'''
        # tif
        path = self.data_path + '/tif/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path)
        list_files_expected = ['image001.tif', 'image002.tif', 'image003.tif']
        list_files = get_sorted_list_images(folder=path)
        self.assertTrue(list_files_expected == list_files)
        
        # fits
        path = self.data_path + '/fits/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path)
        list_files_expected = ['image001.fits', 'image002.fits', 'image003.fits']
        list_files = get_sorted_list_images(folder=path)
        self.assertTrue(list_files_expected == list_files)    
        
      
