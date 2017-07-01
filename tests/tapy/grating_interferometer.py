
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer


class TestClass(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
        
    def test_dict_initialized(self):
        '''assert image, ob and df dicts are correctly initialized'''
        o_grating = GratingInterferometer()
        dict_image = o_grating.dict_image
        self.assertEqual([], dict_image['data'])
        self.assertEqual([], dict_image['file_name'])
        dict_ob = o_grating.dict_ob
        self.assertEqual([], dict_ob['data'])
        self.assertEqual([], dict_ob['file_name'])
        dict_df = o_grating.dict_df
        self.assertEqual([], dict_df['data'])
        self.assertEqual([], dict_df['file_name'])
        
        
    #def test_bad_file_name_raise_ioerror(self):
        #"""assert error is raised when wrong input data file name is given"""
        #_bad_file_name = 'file.fits'
        #o_grating = GratingInterferometer()
        #self.assertRaises(OSError, o_grating.old_load, _bad_file_name)
        
    #def test_empty_file_name_raise_ioerror(self):
        #'''assert error is raised when no input data is given'''
        #o_grating = GratingInterferometer()
        #self.assertRaises(OSError, o_grating.load)
        
    #def test_loading_sample_fits(self):
        #'''assert fits file is correctd loaded'''
        #fits_file = self.data_path + '/image001.fits'
        #o_grating = GratingInterferometer()
        #o_grating.load(file_name=fits_file)
        #data = o_grating.sample
        #[height, width] = np.shape(data)
        #self.assertEqual(np.shape(data), (5, 5))
        #expected_data = np.ones([5,5])
        #for col in np.arange(5):
            #expected_data[:,col] = col        
        #self.assertTrue((data == expected_data).all())

    #def test_loading_ob_fits(self):
        #'''assert fits file is correctd loaded'''
        #fits_file = self.data_path + '/ob001.fits'
        #o_grating = GratingInterferometer()
        #o_grating.load(file_name=fits_file, data_type='ob')
        #data = o_grating.ob
        #[height, width] = np.shape(data)
        #self.assertEqual(np.shape(data), (5, 5))
        #expected_data = np.ones([5,5])
        #self.assertTrue((data == expected_data).all())

    #def test_loading_format_not_supported(self):
        #'''assert error is raised when format is not supported'''
        #file = self.data_path + '/format_not_supported.txt'        
        #o_grating = GratingInterferometer()
        #self.assertRaises(OSError, o_grating.load, file_name=file)
        
    #def test_loading_sample_tiff(self):
        #'''assert tiff file is corrected loaded'''
        #tif_file = self.data_path + '/image001.tif'
        #o_grating = GratingInterferometer()
        #o_grating.load(file_name=tif_file)
        #data = o_grating.sample
        #[height, width] = np.shape(data)
        #self.assertEqual(np.shape(data), (5, 5))
        #expected_data = np.ones([5,5])
        #for col in np.arange(5):
            #expected_data[:,col] = col        
        #self.assertTrue((data == expected_data).all())
        
    #def test_loading_ob_tiff(self):
        #'''assert tiff file is corrected loaded'''
        #tif_file = self.data_path + '/ob001.tif'
        #o_grating = GratingInterferometer()
        #o_grating.load(file_name=tif_file, data_type='ob')
        #data = o_grating.ob
        #[height, width] = np.shape(data)
        #self.assertEqual(np.shape(data), (5, 5))
        #expected_data = np.ones([5,5])
        #self.assertTrue((data == expected_data).all())

    #def test_dark_field_correction_without_ob(self):
        #'''assert dark field correction is correct when no df file given'''
        #tif_file = self.data_path + '/image001.tif'
        #o_grating = GratingInterferometer()
        #o_grating.load(file_name=tif_file)
        #o_grating.dark_field_correction()
        #data = o_grating.sample
        #[height, width] = np.shape(data)
        #self.assertEqual(np.shape(data), (5, 5))
        #expected_data = np.ones([5,5])
        #for col in np.arange(5):
            #expected_data[:,col] = col        
        #self.assertTrue((data == expected_data).all())
        
    #def test_dark_field_correction_with_ob(self):
        #'''assert dark field correction is correct with df file given'''
        #tif_file = self.data_path + '/image001.tif'
        #tif_ob_file = self.data_path + '/ob001.tif'
        #o_grating = GratingInterferometer()
        #o_grating.load(file_name=tif_file)
        #o_grating.load(file_name=tif_ob_file, data_type='ob')
        #o_grating.dark_field_correction()
        #data = o_grating.sample
        #[height, width] = np.shape(data)
        #self.assertEqual(np.shape(data), (5, 5))
        #sample = np.ones([5,5])
        #for col in np.arange(5):
            #sample[:,col] = col        
        #df = np.ones([5,5])
        #expected_data = sample - df
        #self.assertTrue((data == expected_data).all())
        #pass    