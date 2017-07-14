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
 
    def test_normalization_ran_only_once(self):
        '''assert normalization is only once if force switch not turn on'''
        sample_tif_folder = self.data_path + '/tif/sample'
        ob_tif_folder = self.data_path + '/tif/ob'
    
        # testing sample with norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        roi = ROI(x0=0, y0=0, x1=3, y1=2)
        o_grating.normalization(roi=roi)
        _returned_first_time = o_grating.data['sample']['data'][0]
        o_grating.normalization(roi=roi)
        _returned_second_time = o_grating.data['sample']['data'][0]
        self.assertTrue((_returned_first_time == _returned_second_time).all())        

    def test_normalization_ran_twice_with_force_flag(self):
        '''assert normalization can be ran twice using force flag'''
        sample_tif_folder = self.data_path + '/tif/sample'
        ob_tif_folder = self.data_path + '/tif/ob'
    
        # testing sample with norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        roi = ROI(x0=0, y0=0, x1=3, y1=2)
        o_grating.normalization(roi=roi)
        _returned_first_time = o_grating.data['sample']['data'][0]
        roi = ROI(x0=0, y0=0, x1=2, y1=3)
        o_grating.normalization(roi=roi, force=True)
        _returned_second_time = o_grating.data['sample']['data'][0]
        self.assertFalse((_returned_first_time == _returned_second_time).all())
  
    def test_normalization_works(self):
        '''assert sample and ob normalization works with and without roi'''
        sample_tif_folder = self.data_path + '/tif/sample'
        ob_tif_folder = self.data_path + '/tif/ob'

        # testing sample with norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        roi = ROI(x0=0, y0=0, x1=3, y1=2)
        _sample = o_grating.data['sample']['data'][0]
        _expected = _sample / np.mean(_sample[0:3, 0:4])
        o_grating.normalization(roi=roi)
        _returned = o_grating.data['sample']['data'][0]
        self.assertTrue((_expected == _returned).all())

        # testing sample without norm_roi
        o_grating1 = GratingInterferometer()
        o_grating1.load(folder=sample_tif_folder)
        o_grating1.load(folder=ob_tif_folder, data_type='ob')
        _expected = o_grating1.data['sample']['data'][0]
        o_grating1.normalization()
        _returned = o_grating1.data['sample']['data'][0]
        self.assertTrue((_expected == _returned).all())
        
        # testing ob with norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        norm_roi = ROI(x0=0, y0=0, x1=3, y1=2)
        o_grating.normalization(roi=norm_roi)
        _ob = o_grating.data['ob']['data'][0]
        _expected = _ob / np.mean(_ob[0:3, 0:4])
        _returned = o_grating.data['ob']['data'][0]
        self.assertTrue((_expected == _returned).all())
        
        # testing ob without norm_roi
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_tif_folder)
        o_grating.load(folder=ob_tif_folder, data_type='ob')
        _expected = o_grating.data['ob']['data'][0]
        o_grating.normalization()
        _returned = o_grating.data['ob']['data'][0]
        self.assertTrue((_expected == _returned).all())  
  
 
class TestDFCorrection(unittest.TestCase):
    
    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))  
        
    def test_df_correction_when_no_df(self):
        '''assert sample and ob are inchanged if df is empty'''

        # sample
        path = self.data_path + '/tif/sample'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='sample')
        data_before = o_grating.data['sample']['data'][0]
        o_grating.df_correction()
        data_after = o_grating.data['sample']['data'][0]
        self.assertTrue((data_before == data_after).all())
        
        #ob
        path = self.data_path + '/tif/ob'
        o_grating = GratingInterferometer()
        o_grating.load(folder=path, data_type='ob')
        data_before = o_grating.data['ob']['data'][0]
        o_grating.df_correction()
        data_after = o_grating.data['ob']['data'][0]
        self.assertTrue((data_before == data_after).all())
        
    def test_df_fails_when_not_identical_data_shape(self):
        o_grating = GratingInterferometer()
        sample_1 = np.ones([5,5])
        df_1 = np.ones([6,6])
        o_grating.data['sample']['data'] = sample_1
        o_grating.data['df']['data'] = df_1
        self.assertRaises(IOError, o_grating.df_correction)
        
        o_grating = GratingInterferometer()
        ob_1 = np.ones([6,6])
        o_grating.data['ob']['data'] = sample_1
        o_grating.data['df']['data'] = ob_1
        self.assertRaises(IOError, o_grating.df_correction)

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
        o_grating.df_correction()
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
        _expected_data = np.zeros([5,5])
        _ob_data = o_grating.data['ob']['data'][0]
        self.assertTrue((_expected_data == _ob_data).all())

    def test_df_correction_locked_when_run_twice_without_force_flag(self):
        '''assert df corrction run only one time if force flag is False'''
        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob/'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)
        o_grating.load(folder=ob_path, data_type='ob')
        df_file_1 = self.data_path + '/tif/df/df002.tif'
        df_file_2 = self.data_path + '/tif/df/df003.tif'
        o_grating.load(file=df_file_1, data_type='df')
        o_grating.load(file=df_file_2, data_type='df')
        
        # first iteration
        o_grating.df_correction()
        _sample_first_run = o_grating.data['sample']['data'][0]
        _ob_first_run = o_grating.data['ob']['data'][0]
        
        # second iteration
        o_grating.df_correction()
        _sample_second_run = o_grating.data['sample']['data'][0]
        _ob_second_run = o_grating.data['ob']['data'][0]
         
        self.assertTrue((_sample_first_run == _sample_second_run).all())
        self.assertTrue((_ob_first_run == _ob_second_run).all())
         
    def test_df_correction_run_twice_with_force_flag(self):
        '''assert df corrction run more than once with force flag'''
        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob/'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)
        o_grating.load(folder=ob_path, data_type='ob')
        df_file_1 = self.data_path + '/tif/df/df002.tif'
        df_file_2 = self.data_path + '/tif/df/df003.tif'
        o_grating.load(file=df_file_1, data_type='df')
        o_grating.load(file=df_file_2, data_type='df')
        
        # first iteration
        o_grating.df_correction()
        _sample_first_run = o_grating.data['sample']['data'][0]
        _ob_first_run = o_grating.data['ob']['data'][0]
        _average_df = o_grating.data['df']['data_average']
        
        # second iteration
        o_grating.df_correction(force=True)
        _sample_second_run = o_grating.data['sample']['data'][0]
        _ob_second_run = o_grating.data['ob']['data'][0]

        # expected
        _expected_sample_after_second_run = _sample_first_run - _average_df
        _expected_ob_after_second_run = _ob_first_run - _average_df
         
        self.assertTrue((_sample_second_run == _expected_sample_after_second_run).all())
        self.assertTrue((_ob_second_run == _expected_ob_after_second_run).all())    
         
        
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
        
        # x0 < 0 or x1 > image_width
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        o_grating.load(file=ob_tif_file, data_type='ob')
        roi = ROI(x0=0, y0=0, x1=20, y1=4)
        self.assertRaises(ValueError, o_grating.normalization, roi)
       
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        o_grating.load(file=ob_tif_file, data_type='ob')
        roi = ROI(x0=-1, y0=0, x1=4, y1=4)
        self.assertRaises(ValueError, o_grating.normalization, roi)        
        
        # y0 < 0 or y1 > image_height
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        o_grating.load(file=ob_tif_file, data_type='ob')
        roi = ROI(x0=0, y0=-1, x1=4, y1=4)
        self.assertRaises(ValueError, o_grating.normalization, roi)

        # y1>image_height
        o_grating = GratingInterferometer()
        o_grating.load(file=sample_tif_file, data_type='sample')
        o_grating.load(file=ob_tif_file, data_type='ob')
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
        
class TestOscillation(unittest.TestCase):       

    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))  

    def test_error_raised_if_roi_has_wrong_type(self):
        '''assert ValueError raised if roi is not a ROI object'''
        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.normalization()
        _roi = {'x0':0, 'y0':0, 'x1':4, 'y1':4}
        self.assertRaises(ValueError, o_grating.oscillation, roi=_roi)
        
    def test_oscillation_algorithm_without_roi_without_df(self):
        '''assert oscillation of sample and ob works without roi used'''

        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.normalization()
        o_grating.oscillation()
        
        # sample
        _expected = o_grating.data['sample']['data'][1]
        _expected = np.mean(_expected)
        _returned = o_grating.data['sample']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
        # ob
        _expected = o_grating.data['ob']['data'][1]
        _expected = np.mean(_expected)
        _returned = o_grating.data['ob']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
    def test_oscillation_algorithm_without_roi_without_normalization_without_df(self):
        '''assert oscillation of sample and ob works without roi used and without normalization'''

        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.oscillation()
        
        # sample
        _expected = o_grating.data['sample']['data'][1]
        _expected = np.mean(_expected)
        _returned = o_grating.data['sample']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
        # ob
        _expected = o_grating.data['ob']['data'][1]
        _expected = np.mean(_expected)
        _returned = o_grating.data['ob']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
    def test_oscillation_algorithm_with_roi_with_normalization(self):
        '''assert oscillation of sample and ob works with roi used after normalization'''

        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.normalization()
        [x0,y0,x1,y1] = [0,0,2,2]
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        o_grating.oscillation(roi=_roi)
        
        # sample
        _expected = o_grating.data['sample']['data'][1]
        _expected = np.mean(_expected[y0:y1+1, x0:x1+1])
        _returned = o_grating.data['sample']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
        # ob
        _expected = o_grating.data['ob']['data'][1]
        _expected = np.mean(_expected[y0:y1+1, x0:x1+1])
        _returned = o_grating.data['ob']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
    def test_oscillation_algorithm_with_roi_without_df_without_normalization(self):
        '''assert oscillation of sample and ob works with roi used without running normalization'''

        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        [x0,y0,x1,y1] = [0,0,2,2]
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        o_grating.oscillation(roi=_roi)
        
        # sample
        _expected = o_grating.data['sample']['data'][1]
        _expected = np.mean(_expected[y0:y1+1, x0:x1+1])
        _returned = o_grating.data['sample']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
        # ob
        _expected = o_grating.data['ob']['data'][1]
        _expected = np.mean(_expected[y0:y1+1, x0:x1+1])
        _returned = o_grating.data['ob']['oscillation'][1]
        self.assertTrue(_expected == _returned)

    def test_oscillation_algorithm_with_roi_without_normalization_with_df(self):
        '''assert oscillation of sample and ob works with roi,  without normalization, with DF'''

        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.df_correction()
        [x0,y0,x1,y1] = [0,0,2,2]
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        o_grating.oscillation(roi=_roi)
        
        # sample
        _expected = o_grating.data['sample']['data'][1]
        _expected = np.mean(_expected[y0:y1+1, x0:x1+1])
        _returned = o_grating.data['sample']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        
        # ob
        _expected = o_grating.data['ob']['data'][1]
        _expected = np.mean(_expected[y0:y1+1, x0:x1+1])
        _returned = o_grating.data['ob']['oscillation'][1]
        self.assertTrue(_expected == _returned)
        

class TestBinning(unittest.TestCase):       

    def setUp(self):    
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, '../data/'))  
        
    def test_error_raised_if_bin_argument_missing_or_wrong_type(self):
        '''assert ValueError raised if bin argument missing or wrong type'''
        sample_path = self.data_path + '/tif/sample/'
        ob_path = self.data_path + '/tif/ob'
        df_path = self.data_path + '/tif/df'
        
        # missing bin argument
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.df_correction()
        [x0,y0,x1,y1] = [0,0,2,2]
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        o_grating.oscillation(roi=_roi)
        self.assertRaises(ValueError, o_grating.binning)
        
        # bin argument has wrong type
        o_grating = GratingInterferometer()
        o_grating.load(folder=sample_path)      
        o_grating.load(folder=ob_path, data_type='ob')      
        o_grating.load(folder=df_path, data_type='df')
        o_grating.df_correction()
        [x0,y0,x1,y1] = [0,0,2,2]
        _roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        o_grating.oscillation(roi=_roi)
        bin_value = 'bad_type'
        self.assertRaises(ValueError, o_grating.binning)        
        
    def test_error_raised_if_binning_has_no_data_and_ob(self):
        '''assert error raised if we do not have any sample or ob to bin'''
        image1 = self.data_path + '/tif/sample/image001.tif'
        ob1 = self.data_path + '/different_format/ob001_4_by_4.tif'
        
        # no sample and ob
        o_grating = GratingInterferometer()
        self.assertRaises(IOError, o_grating.binning, bin=2)
        
        # no ob
        o_grating = GratingInterferometer()
        o_grating.load(file=image1)
        self.assertRaises(IOError, o_grating.binning, bin=2)
        
        # no sample
        o_grating = GratingInterferometer()
        o_grating.load(file=ob1, data_type='ob')
        self.assertRaises(IOError, o_grating.binning, bin=2)

    def test_binning_works_with_various_bins(self):
        '''assert binning works with various bin size'''
        image1 = self.data_path + '/tif/sample/image001.tif'
        ob1 = self.data_path + '/tif/ob/ob001.tif'
    
        # case 1
        bin = 2 
        o_grating = GratingInterferometer()
        o_grating.load(file=image1)
        o_grating.load(file=ob1, data_type='ob')
        o_grating.binning(bin=bin)
        
        #sample
        _returned_sample = o_grating.data['sample']['data']
        _expected_sample = np.array([[2, 2.5],[1, 2.5]], dtype=np.float32)
        self.assertTrue((_returned_sample == _expected_sample).all())

        #ob
        _returned_ob = o_grating.data['ob']['data']
        _expected_ob = np.array([[2, 1],[1, 1]], dtype=np.float32)
        self.assertTrue((_returned_ob == _expected_ob).all())
        
        # case 2
        bin = 3 
        o_grating = GratingInterferometer()
        o_grating.load(file=image1)
        o_grating.load(file=ob1, data_type='ob')
        o_grating.binning(bin=bin)

        # sample
        _returned_sample = o_grating.data['sample']['data']
        _expected_sample = np.array([1.7777778], dtype=np.float32)
        self.assertAlmostEqual(_returned_sample, _expected_sample, delta=0.0001)

        # ob
        _returned_ob = o_grating.data['ob']['data']
        _expected_ob = np.array([1.4444443], dtype=np.float32)
        self.assertAlmostEqual(_returned_ob, _expected_ob, delta=0.0001)
    
    #def test_bin_can_only_ran_one_time_without_force_flag(self):
        #'''assert the bin algorithm is only run one time if force flag is False'''
        #sample_path = self.data_path + '/tif/sample/'
        #ob_path = self.data_path + '/tif/ob'
        #df_path = self.data_path + '/tif/df'
        #o_grating = GratingInterferometer()
        #o_grating.load(folder=sample_path)      
        #o_grating.load(folder=ob_path, data_type='ob')      
        #o_grating.load(folder=df_path, data_type='df')
        #o_grating.df_correction()
        #[x0,y0,x1,y1] = [0,0,2,2]
        #_roi = ROI(x0=x0, y0=y0, x1=x1, y1=y1)
        #o_grating.oscillation(roi=_roi)
        
        ## first time running algorithm
        #o_grating.binning()
        #_sample_data_first_time = o_grating.data['sample']['data']
        #o_grating.binning()
        #_sample_data_second_time = o_grating.data['sample']['data']
        
        #print(_sample_data_first_time)
        #print(_sample_data_second_time)
        #self.assertTrue(False)
        