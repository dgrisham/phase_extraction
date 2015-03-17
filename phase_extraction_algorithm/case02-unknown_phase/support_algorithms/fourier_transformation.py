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
from numpy import array, roll, lib, delete
import numpy as np
import numpy.fft as fft


'''
        The Fourier transform function in Mathematica is the same as the one 
        Python uses when coupled with FourierParameters[1,-1]. See 
        "Mathematica_FFT.png" file for more information. It's nice to be able 
        to compare the results computed by Python against some other programs.
'''


################## Perform the Fourier transformation ################
'Perform the Fourier transform'
def FFT(data, xPixel, dxPixel):
        '''
                FFT of the Numpy package in Python behaves a little different
                from Mathematica's Fourier function. For Mathematica, one has 
                to specify which FourierParameters to use. For signal processing,
                it's [1,-1].
        '''

        # Compute the Fourier transform of the input data
        transData = fft.fft2(data)

        '''
                The goal is to shift zero frequency components to the center
                of the image. They are where the phase of the original data is.
        '''

        # Shift zero frequency modes to the center
        transData = fft.fftshift(transData)

        # Translate to real distance
        transData = xPixel * dxPixel**2. * transData

        # Return the Fourier-transformed data
        return transData


################## Padding the FFT side lobe image  ##################
'Pad zeros into empty space'
def padwithzeros(vector, pad_width, iaxis, kwargs):
    vector[:pad_width[0]] = 0.0
    vector[-pad_width[1]] = 0.0
    return vector

'Fix the dimension after padding'
def fixDim(data, xPixel):
        # Pad the existing matrix with zeros in both x and y directions
        padding = lib.pad(data, xPixel/2 - len(data)/2, padwithzeros)

        # Fix the dimension of the matrix that matches the original image
        if len(data) % 2 == 1:
                # Delete the last column
                padding = delete(padding, -1, axis=1)
                # Delete the first row
                padding = delete(padding, -1, axis=0)

        # Return the fixed dimension matrix
        return padding


############# Perform the inverse Fourier transform ##################
'Perform the inverse Fourier transform'
def invFFT(dataFFT, xPixel, dxPixel):
        '''
                Before we can compute the inverse Fourier transform, 
                shift the zero frequency back.
        '''

        # Shift zero frequency modes back
        dataFFT = fft.ifftshift(dataFFT)

        # Compute the inverse Fourier transform of the input data
        invTransData = fft.ifft2(dataFFT)

        # Translate to real distance
        invTransData = invTransData/(xPixel * dxPixel**2.)

        # Return the inverse Fourier-transformed data
        return invTransData
