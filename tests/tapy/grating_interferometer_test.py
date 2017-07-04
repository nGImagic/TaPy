
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
        data = o_grating.data
        dict_image = o_grating.dict_image
        self.assertEqual([], dict_image['data'])
        self.assertEqual([], dict_image['file_name'])
        self.assertEqual([], data['sample']['data'])
        self.assertEqual([], data['sample']['file_name'])
        
        dict_ob = o_grating.dict_ob
        self.assertEqual([], dict_ob['data'])
        self.assertEqual([], dict_ob['file_name'])
        self.assertEqual([], data['ob']['data'])
        self.assertEqual([], data['ob']['file_name'])

        dict_df = o_grating.dict_df
        self.assertEqual([], dict_df['data'])
        self.assertEqual([], dict_df['file_name'])
        self.assertEqual([], data['df']['data'])
        self.assertEqual([], data['df']['file_name'])
        
    def test_loading_bad_single_files(self):
        '''assert error is raised when inexisting file is given'''
        bad_tiff_file_name = 'bad_tiff_file_name.tiff'
        o_grating = GratingInterferometer()
        self.assertRaises(OSError, o_grating.load, bad_tiff_file_name, '', 'sample')
        self.assertRaises(OSError, o_grating.load, bad_tiff_file_name, '', 'ob')
        self.assertRaises(OSError, o_grating.load, bad_tiff_file_name, '', 'df')
        bad_fits_file_name = 'bad_fits_file_name.fits'
        o_grating = GratingInterferometer()
        self.assertRaises(OSError, o_grating.load, bad_fits_file_name, '', 'sample')
        self.assertRaises(OSError, o_grating.load, bad_fits_file_name, '', 'ob')
        self.assertRaises(OSError, o_grating.load, bad_fits_file_name, '', 'df')
        bad_h5_file_name = 'bad_h5_file_name.h5'
        self.assertRaises(OSError, o_grating.load, bad_h5_file_name, '', 'sample')
        self.assertRaises(OSError, o_grating.load, bad_h5_file_name, '', 'ob')
        self.assertRaises(OSError, o_grating.load, bad_h5_file_name, '', 'df')
        
    def test_loading_good_single_file(self):
        '''assert sample, ob and df single file correctly loaded'''
        # tiff
        sample_tif_file = self.data_path + '/tif//sample/image001.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        _expected_data = np.ones([5,5])
        _expected_data[0,0] = 5
        _loaded_data = o_grating.data['sample']['data']
        self.assertTrue((_expected_data == _loaded_data).all())
        _expected_name = sample_tif_file
        _loaded_name = o_grating.data['sample']['file_name'][0]
        self.assertTrue(_expected_name == _loaded_name)

        # fits
        sample_fits_file = self.data_path + '/fits//sample/image001.fits'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_fits_file, data_type='sample')
        _expected_data = np.ones([5,5])
        _expected_data[0,0] = 5
        _expected_data[:,2] = 2
        _expected_data[:,3] = 3
        _expected_data[:,4] = 4
        _loaded_data = o_grating.data['sample']['data']
        self.assertTrue((_expected_data == _loaded_data).all())
        _expected_name = sample_fits_file
        _loaded_name = o_grating.data['sample']['file_name'][0]
        self.assertTrue(_expected_name == _loaded_name)
        
    def test_loading_good_several_single_files(self):
        '''assert sample, ob and df multi files correctly loaded'''
        # tiff
        sample_tif_file_1 = self.data_path + '/tif//sample/image001.tif'
        sample_tif_file_2 = self.data_path + '/tif/sample/image002.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file_1, data_type='sample')
        o_grating.load(file=sample_tif_file_2, data_type='sample')

        _expected_data_1 = np.ones([5,5])
        _expected_data_1[0,0] = 5
        _loaded_data_1 = o_grating.data['sample']['data'][0]
        self.assertTrue((_expected_data_1 == _loaded_data_1).all())
        _expected_name_1 = sample_tif_file_1
        _loaded_name_1 = o_grating.data['sample']['file_name'][0]
        self.assertTrue(_expected_name_1 == _loaded_name_1)
        
        _expected_data_2 = np.ones([5,5])
        _expected_data_2[0,0] = 5
        _expected_data_2[:,2:4] = 3
        _loaded_data_2 = o_grating.data['sample']['data'][1]
        self.assertTrue((_expected_data_2 == _loaded_data_2).all())
        _expected_name_2 = sample_tif_file_2
        _loaded_name_2 = o_grating.data['sample']['file_name'][1]
        self.assertTrue(_expected_name_2 == _loaded_name_2)        
        
        # fits
        sample_fits_file_1 = self.data_path + '/fits//sample/image001.fits'
        sample_fits_file_2 = self.data_path + '/fits/sample/image002.fits'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_fits_file_1, data_type='sample')
        o_grating.load(file=sample_fits_file_2, data_type='sample')
    
        _expected_data_1 = np.ones([5,5])
        _expected_data_1[0,0] = 5
        _expected_data_1[:,2] = 2
        _expected_data_1[:,3] = 3
        _expected_data_1[:,4] = 4
        _loaded_data_1 = o_grating.data['sample']['data'][0]
        self.assertTrue((_expected_data_1 == _loaded_data_1).all())
        _expected_name_1 = sample_fits_file_1
        _loaded_name_1 = o_grating.data['sample']['file_name'][0]
        self.assertTrue(_expected_name_1 == _loaded_name_1)
    
        _expected_data_2 = np.ones([5,5])
        _expected_data_2[0,0] = 5
        _expected_data_2[:,2] = 2
        _expected_data_2[:,3] = 3
        _expected_data_2[:,4] = 4
        _loaded_data_2 = o_grating.data['sample']['data'][1]
        self.assertTrue((_expected_data_2 == _loaded_data_2).all())
        _expected_name_2 = sample_fits_file_2
        _loaded_name_2 = o_grating.data['sample']['file_name'][1]
        self.assertTrue(_expected_name_2 == _loaded_name_2)             
        
    def test_all_images_names_retrieved_from_file(self):
        '''assert list of images are correctly retrieved from individual file name'''
        # tif
        path = self.data_path + '/tif/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path)
        list_files_expected = ['image001.tif', 'image002.tif', 'image003.tif']
        list_files = o_grating.get_sorted_list_images(folder=path)
        self.assertTrue(list_files_expected == list_files)
        
        # fits
        path = self.data_path + '/fits/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path)
        list_files_expected = ['image001.fits', 'image002.fits', 'image003.fits']
        list_files = o_grating.get_sorted_list_images(folder=path)
        self.assertTrue(list_files_expected == list_files)

    def test_all_images_names_retrieved_from_folder(self):
        '''assert list_of images are correctly loaded when retrieved from folder'''
        # tif
        path = self.data_path + '/tif/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='sample')
        list_of_files = ['image001.tif', 'image002.tif', 'image003.tif']
        list_of_files_expected = [os.path.join(path, _file) for _file in list_of_files]
        list_of_files_retrieved = o_grating.data['sample']['file_name']
        self.assertTrue(list_of_files_expected == list_of_files_retrieved)
        
        #fits
        path = self.data_path + '/fits/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='sample')
        list_of_files = ['image001.fits', 'image002.fits', 'image003.fits']
        list_of_files_expected = [os.path.join(path, _file) for _file in list_of_files]
        list_of_files_retrieved = o_grating.data['sample']['file_name']
        self.assertTrue(list_of_files_expected == list_of_files_retrieved)
        
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