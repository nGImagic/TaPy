
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer
from tapy._utilities import get_sorted_list_images, average_df, remove_inf_null


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
        
    def test_df_averaging(self):
        '''assert df average works'''
        df_tif_file_2 = self.data_path + '/tif/df/df002.tif'
        df_tif_file_3 = self.data_path + '/tif/df/df003.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=df_tif_file_2, data_type='df')
        o_grating.load(file=df_tif_file_3, data_type='df')
        _average_df = average_df(df=o_grating.data['df']['data'])
        expected_df = np.ones([5,5])
        expected_df[0,0] = 5
        self.assertTrue((expected_df == _average_df).all())    
      
    def test_remove_inf_null(self):
        '''assert remove inf and null works'''
        
        # no 0 and no inf
        before_data_1 = np.ones((5,5))
        after_data_1 = remove_inf_null(data=before_data_1)
        self.assertTrue((before_data_1 == after_data_1).all())
        
        # with 0
        before_data_2 = np.ones((5,5))
        before_data_2[3,3] = 0
        after_data_2 = remove_inf_null(data=before_data_2)
        _expected_data_2 = before_data_2.copy()
        _expected_data_2[3,3] = np.NaN
        np.testing.assert_array_equal(_expected_data_2, after_data_2)
        
        # with np.inf
        before_data_3 = np.ones((5,5))
        before_data_3[2,2] = np.inf
        after_data_3 = remove_inf_null(data=before_data_3)
        _expected_data_3 = before_data_3.copy()
        _expected_data_3[2,2] = np.NaN
        np.testing.assert_array_equal(_expected_data_3, after_data_3)