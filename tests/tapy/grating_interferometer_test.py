
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer


class TestLoadingNormalization(unittest.TestCase):
    
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
        _expected_data[:,2] = 2
        _expected_data[:,3] = 3
        _expected_data[:,4] = 4
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
        _expected_data_1[:,2] = 2
        _expected_data_1[:,3] = 3
        _expected_data_1[:,4] = 4
        _loaded_data_1 = o_grating.data['sample']['data'][0]
        self.assertTrue((_expected_data_1 == _loaded_data_1).all())
        _expected_name_1 = sample_tif_file_1
        _loaded_name_1 = o_grating.data['sample']['file_name'][0]
        self.assertTrue(_expected_name_1 == _loaded_name_1)
        
        _expected_data_2 = np.ones([5,5])
        _expected_data_2[0,0] = 5
        _expected_data_2[:,2] = 2
        _expected_data_2[:,3] = 3
        _expected_data_2[:,4] = 4
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
        
    def test_normalization_raises_error_if_no_ob_or_sample(self):
        '''assert error raises when no ob or sample provided'''
        path = self.data_path + '/tif/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='sample')
        self.assertRaises(IOError, o_grating.normalization)
        
        path = self.data_path + '/tif/ob'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='ob')
        self.assertRaises(IOError, o_grating.normalization)
        
        sample_path = self.data_path + '/tif/sample'
        ob_path = self.data_path + '/tif/ob'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path, data_type='sample')
        o_grating.load(folder=ob_path, data_type='ob')
        assert o_grating.normalization()
        
    def test_df_correction_when_no_df(self):
        '''assert sample and ob are inchanged if df is empty'''
        path = self.data_path + '/tif/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='sample')
        data_before = o_grating.data['sample']['data'][0]
        o_grating.df_correction(data_type='sample')
        data_after = o_grating.data['sample']['data'][0]
        self.assertTrue((data_before == data_after).all())
        
        path = self.data_path + '/tif/ob'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='ob')
        data_before = o_grating.data['ob']['data'][0]
        o_grating.df_correction(data_type='sample')
        data_after = o_grating.data['ob']['data'][0]
        self.assertTrue((data_before == data_after).all())
        
    def test_right_data_type_passed_to_df_correction(self):
        '''assert data_type is either sample or ob'''
        sample_path = self.data_path + '/tif/sample'
        df_path = self.data_path + '/tif/df'        
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path, data_type='sample')
        o_grating.load(folder=df_path, data_type='df')
        self.assertRaises(KeyError, o_grating.df_correction, 'not_data_type')
        
    def test_df_fails_when_not_identical_data_shape(self):
        o_grating = GratingInterferometer()
        sample_1 = np.ones([5,5])
        df_1 = np.ones([6,6])
        o_grating.data['sample']['data'] = sample_1
        o_grating.data['df']['data'] = df_1
        self.assertRaises(IOError, o_grating.df_correction, 'sample')
        
        o_grating = GratingInterferometer()
        ob_1 = np.ones([6,6])
        o_grating.data['ob']['data'] = sample_1
        o_grating.data['df']['data'] = ob_1
        self.assertRaises(IOError, o_grating.df_correction, 'ob')
        
    def test_same_number_of_images_loaded_in_sample_and_ob(self):
        '''assert sample and ob have the same number of images loaded'''
        sample_tif_file_1 = self.data_path + '/tif/sample/image001.tif'
        sample_tif_file_2 = self.data_path + '/tif/sample/image002.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file_1, data_type='sample')
        o_grating.load(file=sample_tif_file_2, data_type='sample')
        ob_tif_file_1 = self.data_path + '/tif/ob/ob001.tif'
        o_grating.load(file=ob_tif_file_1, data_type='ob')
        self.assertRaises(IOError, o_grating.normalization)
        
    def test_df_averaging(self):
        '''assert df average works'''
        df_tif_file_2 = self.data_path + '/tif/df/df002.tif'
        df_tif_file_3 = self.data_path + '/tif/df/df003.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=df_tif_file_2, data_type='df')
        o_grating.load(file=df_tif_file_3, data_type='df')
        average_df = o_grating._average_df(df=o_grating.data['df']['data'])
        expected_df = np.ones([5,5])
        expected_df[0,0] = 5
        self.assertTrue((expected_df == average_df).all())

    def test_df_averaging_only_run_the_first_time(self):
        '''assert the average_df is only run the first time the df_correction is run'''
        pass

    def test_df_correction(self):
        '''assert df corrction works'''
        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob/'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)
        o_grating.load(folder=ob_path, data_type='ob')
        df_file_1 = self.data_path + '/tif/df/df002.tif'
        df_file_2 = self.data_path + '/tif/df/df003.tif'
        o_grating.load(file=df_file_1, data_type='df')
        o_grating.load(file=df_file_2, data_type='df')
        o_grating.df_correction()
        _expected_data = np.zeros([5,5])
        _expected_data[:,2] = 1
        _expected_data[:,3] = 2
        _expected_data[:,4] = 3       
        _sample_data = o_grating.data['sample']['data'][0]
        self.assertTrue((_expected_data == o_grating.data['sample']['data'][0]).all())