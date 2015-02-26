'''
    Collaborators: Lam H. Mach & David Grisham
    Engineering Physics 2016
    Date: 02/22/2015
    Faculty Adviser: Dr. Charles Durfee
    Department of Physics
    Colorado School of Mines
'''


################# Import modules and Python packages #################
# Computation
from numpy import array, angle
import numpy as np
# Image processing
import Image, ImageEnhance
# Set the directory of stored images
import os


'''
        This file is used for image processing. For the ease of use and 
        maintenance, the "Image" Python package for image processing was 
        used. This package is included in "Anaconda" scientific package 
        available through the continuum's website. The link is:
                "https://store.continuum.io/cshop/anaconda/" 
'''


####################### Input and output images ######################
'List of images'
images = array(["Step_01-Interferogram.jpg",
                                "Step_02-FFT_Interferogram.jpg",
                                "Step_03-Power_Spectrum_Interferogram.jpg",
                                "Step_04-Sidelob_Density.jpg",
                                "Step_05-Power_Spectrum_Side_Lob.jpg",
                                "Step_06-invFFT_Interferogram.jpg",
                                "Step_07-Phase_Interferogram.jpg"
                                ])

'Open an image'
def imageIn(step, path):
        # Combine the path
        path = path + images[step]

        # Open an image corresponding to its position in images list
        image = Image.open(path)
        return image, path


################## Enhance the input and output images ###############
'Adjust the brightness'
def enhancer(image, brightness, folder):
        # Image path
        path = os.getcwd()[:-19] + folder

        # Input the image
        I, path = imageIn(image, path)

        # Pass the image to the ImageEnhance function in Image package
        enhance = ImageEnhance.Brightness(I)

        # Pass the new brightness to the image
        brighterImage = enhance.enhance(brightness)

        # Return the newly enhanced image
        brighterImage.save(path)
