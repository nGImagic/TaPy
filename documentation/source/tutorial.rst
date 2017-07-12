Tutorial
========

First you need to install the TaPy library

$ pip install tapy

Then in your python environment, import TaPy

>>> import tapy

First thing to do is to let the program know where are the sample, open beam (OB) and dark field (DF) images. 
Two options are available to load them:

* file by file
* full folder at once
  
Loading images file by file
---------------------------

Let's pretend that our images are in the folder **/Users/me/sample/** and named 

- image001.fits
- image002.fits
- image003.fits

>>> o_grating = tapy.GratingInterferometer()
>>> o_grating.load(file='/Users/me/sample/image001.fits', data_type='sample')
>>> o_grating.load(file='/Users/me/sample/image002.fits', data_type='sample')
>>> o_grating.load(file='/Users/me/sample/image003.fits', data_type='sample')

At this point all the data have been loaded in memory and can be accessed as followed

>>> image001 = o_grating.data['sample']['data'][0]
>>> image002 = o_grating.data['sample']['data'][1]

and the file names

>>> image003_file_name = o_grating.data['sample']['file_name'][2]

Let's use the second method to retrieve files for the OB

Loading all images at once
--------------------------

Our OB are in the folder **/Users/me/ob/** and named

- ob001.fits
- ob002.fits
- ob003.fits

>>> o_grating.load(folder='/Users/me/ob', data_type='ob')

again, all the data can be retrieved as followed

>>> ob1 = o_grating.data['ob']['data'][0]
>>> ob2_file_name = o_grating.data['ob']['file_name'][1]

For this library, DF are optional but for the sake of this exercise, let's load them 

>>> o_grating.load(folder='/Users/me/df', data_type='df')

WARNING:
From this point, any operation on your data will overwrite the inital data loaded. Those
data can be retrieved at any point by doing

>>> data = o_grating.data['sample']['data']
>>> ob = o_grating.data['ob']['data']

Dark Field Correction
---------------------

If you loaded a set of Dark Field (DF) images, you probably want to correct all your
images (sample and OB) for dark field correction

>>> o_grating.df_correction()

In case you did not loaded a set of DF, this correction will leave the images untouched

Normalization using ROI (optional)
----------------------------------

If you want to specify a region of your sample to match with the OB

Let's use the following region 

- x0 = 10
- y0 = 10
- x1 = 50
- y1 = 50

>>> my_norm_roi = tapy.ROI(x0=10, y0=10, x1=50, y1=50)

then the normalization can be run

>>> o_grating.normalization(norm_roi=my_norm_roi)

Normalization
-------------

If you don't want any normalization ROI, simply run the normalization

>>> o_grating.normalization()

How to get the normalized data
------------------------------

Each of the data set in the sample and ob will then be normalized.
If a norm_roi has been provided, the sample arrays will be divided by the average of the 
region defined. Same thing for the ob. Those normalized array can be retrieved this way

>>> sample_normalized_array = o_grating.data['sample']['data']
>>> ob_normalized_array = o_gretting.data['ob']['data']

Cropping the data (optional)
----------------------------

You have the option to crop the data but if you do, this must be done after running the normalization. 
The algorithm only cropped the normalized sample and ob data

- the 4 corners of the region of interest (ROI)
- the top left corner coordinates, width and height of the ROI

let's use the first method and let's pretend the ROI is defined by

- x0 = 5
- y0 = 5
- x1 = 200
- y1 = 250

>>> my_crop_roi = tapy.ROI(x0=5, y0=5, x1=200, y1=250)
>>> o_grating.crop(roi=my_crop_roi)

Oscillation
-----------

Now we gonna check the mean value of the region of interest selected for each of the sample and ob data.
If you don't specify a ROI, the entire image will be used.

Let's use a ROI defined as follow

- x0 = 0
- y0 = 0
- x1 = 50
- y1 = 50

>>> my_oscillation_roi = ROI(x0=0, y0=0, x1=50, y1=50)
>>> o_grating.oscillation(roi=my_oscillation_roi)

We can now retrieve the sample and ob data

>>> sample_oscillation = o_grating.data['sample']['oscillation']
>>> ob_oscillation = o_grating.data['ob']['oscillation']

We can now display the oscillation data
