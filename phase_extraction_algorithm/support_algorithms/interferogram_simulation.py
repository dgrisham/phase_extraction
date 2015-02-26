'''
    Collaborators: Lam H. Mach & David Grisham
    Engineering Physics 2016
    Date: 02/22/2015
    Faculty Adviser: Dr. Charles Durfee
    Department of Physics
    Colorado School of Mines
'''


################# Import modules and Python packages #################
'Import Python packages'
# Computation
from numpy import array, exp, sin
import numpy as np
# Plotting
import matplotlib.pyplot as plt
import matplotlib as mp


'''
        This file simulates the interferometry pattern using given parameters.
        It's only used for testing purpose.
'''


##################### Set up the interferogram #######################
'Define constants and parameters'
# Speed of light in vacuum
c = 3.*pow(10, 8.)

'Conversion of unit'
def convert(x, unit):
        # Convert unit to m
        if unit == 'mm':
                return x * pow(10, -3.)
        elif unit == 'um':
                return x * pow(10, -6.)
        elif unit == 'nm':
                return x * pow(10, -9.)

        # Convert unit to radian
        elif unit == 'mRad':
                return x * pow(10, -3.)
        elif unit == 'uRad':
                return x * pow(10, -6.)
        elif unit == 'nRad':
                return x * pow(10, -9.)

        # Otherwise
        else:
                print "Please update the convert def"

'Set the rounding option for Numpy array'
def roundup(x, decimal_places):
        return np.around(x, decimals = decimal_places)

'Phase function'
def phi(x, y, factors):
        return factors[0] * (x**2. + y**2.) + factors[1] * sin(factors[2] * y)

'Calculate the intensity'
def intensity(x, y, a1, a2, w, w0, theta0, factors):
        '''
                Sign of retrieved phases depends on the chosen side lode 
        '''
        # Amplitudes
        a1 = a1 * exp(-(x**2. + y**2.)/(w**2.))
        a2 = a2 * exp(-(x**2. + y**2.)/(w**2.))

        # Electric fields with E_2 is the reference beam
        E1 = a1 * exp(1j * (w0/c * sin(theta0) * x + phi(x, y, factors)))
        E2 = a2 * exp(-1j * (w0/c * sin(theta0) * x))

        # Simulated phases (stored for later comparison)
        realPhase = phi(x, y, factors)

        # Calculate the intensity comprised of these 2 electric fields
        return abs(E1 + E2)**2., realPhase

'Intensity profile definition'
def intensityProfile(xPixel, yPixel, xRealDis, yRealDis, constants):
        # Real distance corresponding to 1 pixel
        dxPixel = xRealDis/xPixel
        dyPixel = yRealDis/yPixel

        # Set up lists of pixel_to_distance data
        xPixelL = array([(i - xPixel/2.) * dxPixel for i in xrange(1, xPixel + 1)])
        yPixelL = array([(i - yPixel/2.) * dyPixel for i in xrange(1, yPixel + 1)])     

        # Set up the intensity grid (2 x 2 matrix)
        I = array([[0.] * xPixel] * yPixel)

        # Set up the phase grid
        realPhaseList = array([[0.] * xPixel] * yPixel)

        # Compute intensity and pass the result to the intensity matrix
        for i in xrange(yPixel):
                for j in xrange(xPixel):
                        I[i, j], realPhaseList[i, j] = intensity(xPixelL[j], yPixelL[i], 
                                                                                                         constants[0], constants[1],
                                                                                                         constants[2], constants[3],
                                                                                                         constants[4], constants[5])

        # Return the intensity profile
        return I, xPixelL, yPixelL, realPhaseList
