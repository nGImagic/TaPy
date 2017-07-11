
import unittest
import numpy as np
import os
from PIL import Image

from tapy.grating_interferometer import GratingInterferometer
from tapy.roi import ROI


class TestNormalization(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))
        
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
 
class TestDFCorrection(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))  
        
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

    def test_df_averaging_only_run_the_first_time(self):
        '''assert the average_df is only run the first time the df_correction is run'''
        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob/'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)
        o_grating.load(folder=ob_path, data_type='ob')
        df_file_1 = self.data_path + '/tif/df/df002.tif'
        df_file_2 = self.data_path + '/tif/df/df003.tif'
        o_grating.load(file=df_file_1, data_type='df')
        o_grating.load(file=df_file_2, data_type='df')
    
        df_average_data = o_grating.data['df']['data_average']
        self.assertTrue(df_average_data == [])
    
        #sample
        o_grating.df_correction()
        df_average_data = o_grating.data['df']['data_average']
        self.assertTrue(df_average_data != [])
    
        #ob
        o_grating.df_correction(data_type='ob')
        expected_df_average = df_average_data
        df_average = o_grating.data['df']['data_average']
        self.assertTrue((expected_df_average == df_average).all())

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
        
        #sample
        o_grating.df_correction()
        _expected_data = np.zeros([5,5])
        _expected_data[:,2] = 1
        _expected_data[:,3] = 2
        _expected_data[:,4] = 3       
        _sample_data = o_grating.data['sample']['data'][0]
        self.assertTrue((_expected_data == o_grating.data['sample']['data'][0]).all())
        
        #ob
        o_grating.df_correction(data_type='ob')
        _expected_data = np.zeros([5,5])
        _ob_data = o_grating.data['ob']['data'][0]
        self.assertTrue((_expected_data == _ob_data).all())

    def test_sample_df_correction(self):
        '''assert sample df correction works with and without norm roi provided'''
        sample_tif_folder = self.data_path + '/tif/sample'
        ob_tif_folder = self.data_path + '/tif/ob'

        # testing sample with norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        roi = ROI(x0=0, y0=0, x1=3, y1=2)
        o_grating.normalization(roi=roi)
        _sample = o_grating.data['sample']['data'][0]
        _expected = _sample / np.mean(_sample[0:3, 0:4])
        _returned = o_grating.data['sample']['normalized'][0]
        self.assertTrue((_expected == _returned).all())

        # testing sample without norm_roi
        o_grating1 = GratingInterferometer()
        o_grating1.load(folder=sample_tif_folder)
        o_grating1.load(folder=ob_tif_folder, data_type='ob')
        o_grating1.normalization()
        _expected = o_grating1.data['sample']['data'][0]
        _returned = o_grating1.data['sample']['normalized'][0]
        self.assertTrue((_expected == _returned).all())
        
        # testing ob with norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        norm_roi = ROI(x0=0, y0=0, x1=3, y1=2)
        o_grating.normalization(roi=norm_roi)
        _ob = o_grating.data['ob']['data'][0]
        _expected = _ob / np.mean(_ob[0:3, 0:4])
        _returned = o_grating.data['ob']['normalized'][0]
        self.assertTrue((_expected == _returned).all())
        
        # testing ob without norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        o_grating.normalization()
        _expected = o_grating.data['ob']['data'][0]
        _returned = o_grating.data['ob']['normalized'][0]
        self.assertTrue((_expected == _returned).all())        
        
class TestApplyingROI(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))       
        
    def test_roi_type_in_normalization(self):
        '''assert error is raised when type of norm roi are not ROI in normalization'''
        sample_tif_file = self.data_path + '/tif/sample/image001.tif'
        ob_tif_file = self.data_path + '/tif/ob/ob001.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        o_grating.load(file=ob_tif_file, data_type='ob')
        roi = {'x0':0, 'y0':0, 'x1':2, 'y1':2}
        self.assertRaises(ValueError, o_grating.normalization, roi)
        
    def test_roi_fit_images(self):
        '''assert norm roi do fit the images'''
        sample_tif_file = self.data_path + '/tif/sample/image001.tif'
        ob_tif_file = self.data_path + '/tif/ob/ob001.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        o_grating.load(file=ob_tif_file, data_type='ob')
        
        # x0 < 0 or x1 > image_width
        roi = ROI(x0=0, y0=0, x1=20, y1=4)
        self.assertRaises(ValueError, o_grating.normalization, roi)
        roi = ROI(x0=-1, y0=0, x1=4, y1=4)
        self.assertRaises(ValueError, o_grating.normalization, roi)        
        
        # y0 < 0 or y1 > image_height
        roi = ROI(x0=0, y0=-1, x1=4, y1=4)
        self.assertRaises(ValueError, o_grating.normalization, roi)
        roi = ROI(x0=0, y0=0, x1=4, y1=20)
        self.assertRaises(ValueError, o_grating.normalization, roi)        

    def test_error_raised_when_data_shape_of_different_type_do_not_match(self):
        '''assert shape of data must match to allow normalization'''
        
        # sample and ob
        image1 = self.data_path + '/tif/sample/image001.tif'
        ob1 = self.data_path + '/different_format/ob001_4_by_4.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=image1)
        o_grating.load(file=ob1, data_type='ob')
        self.assertRaises(ValueError, o_grating.normalization)
        
        # sample, ob and df
        image1 = self.data_path + '/tif/sample/image001.tif'
        ob1 = self.data_path + '/tif/ob/ob001.tif'
        df1 = self.data_path + '/different_format/df001_4_by_4.tif'
        o_grating = GratingInterferometer()
        o_grating.load(file=image1)
        o_grating.load(file=ob1, data_type='ob')
        o_grating.load(file=df1, data_type='df')
        self.assertRaises(ValueError, o_grating.normalization)
        
       
