'''
    Collaborators: Lam H. Mach & David Grisham
    Engineering Physics 2016
    Date: 02/27/2015
    Faculty Adviser: Dr. Charles Durfee
    Department of Physics
    Colorado School of Mines
'''


################### Import modules and Python packages ###############
'Import Python packages'
import sys, os
# Image processing
from PIL import Image
# Computation
import numpy as np
from numpy import array, pi, append
from copy import deepcopy
# Plotting
import matplotlib.pyplot as plt

'Import external Python modules'
# Set the modules' directory
sys.path.append(os.path.abspath(os.path.join(os.getcwd())) + "/support_algorithms")
sys.path.append(os.path.abspath(os.path.join(os.getcwd())) + "/image_functions")
# import image processing modules
from image_functions import *
# Import modules for simulating the interferogram
from interferogram_simulation import convert, intensityProfile
# Import modules for plotting
from surface_plot import densityPlot, xyPlot, surfacePlot
# Import modules for performing Fourier transform
from fourier_transformation import FFT, fixDim, invFFT
# Import modules for extracting phase
from phase_retrieval import phaseExtraction, unwrapPhaseProfile
# Import modules for processing images
from image_processing import enhancer, centroidSidelobe, sort
# get path for images
image_path = '../../images'

'''
    This file executes algorithms from files in the "Support_Algorithms"
    folder. All constants are declared within this file. Different versions 
    of this file won't change the core algorithms. If you want to change 
    the algorithm of any process within this file, go to "Support_Algorithms".
'''


################ Set up the interferogram ############################
'Define constants and parameters'
# Speed of light in vacuum
c = 3*pow(10, 8) # m/s

# The laser wavelength
lambda0 = convert(800, 'nm')

# The fundamental frequency
w0 = 2.*pi*c/lambda0 # Hz

# Beam angle from optical axis, (1/2) full angle
theta0 = convert(5., 'mRad')

# Electric fields' amplitudes
a1, a2 = 1, 1

# w factor
w = convert(1000, 'um')

# Spatial frequency of the side lobe
fx0 = w0*theta0/(pi*c)

# alpha and beta factors
a = 5./(w**2)
b = 4.
g = 4./w
factors = [a, b, g]

# List of constants
listConst = [a1, a2, w, w0, theta0, factors]

'Set up the image grid'
# Image size
xPixel, yPixel = 1024, 1024


''' look here, lam '''
# here's where i put in some code.
# first i load the image, then subtract
# off the background. now i'm not sure what
# exactly i want to do. i set the values of
# xPixel and yPixel, that's about it. 
img = import_image(image_path + '/image0.jpg')
bg = import_image(image_path + '/background.jpg')
img = subtract_background(img, bg)
# at this point, 'img' is a 2-d numpy array.
#show_image(img) # uncomment this line to see img
(xPixel, yPixel) = img.shape
xRealDis, yRealDis = 4.*w, 4.*w

'Get the intensity profile'
I, xAxis, yAxis, realPhase = intensityProfile(xPixel, yPixel, xRealDis, 
                                              yRealDis, listConst)

'Store the x and y values'
xAxisStored = xAxis
yAxisStored = yAxis

'Plot the simulated interferogram from given parameters'
# Set necessary parameters
title = r'The Simulated Interferogram (mm)'
saveDirectory = "./results/step_01-interferogram.jpg"
style = 'Greys'
interpolation = 'gaussian'
show = 0

# Plot the density map of the interferogram
densityPlot(I, xAxis, yAxis, title, style, interpolation, saveDirectory, show)


################## Fourier transformation ############################
'Perform the Fourier transform'
transI = FFT(I, xPixel, xRealDis/xPixel)

'Plot the FFT of the given interferogram'
# Set necessary parameters
title = r'The FFT of The Simulated Interferogram (mm)'
saveDirectory = "./results/step_02-fft_interferogram.jpg"
style = None
interpolation = 'gaussian'
show = 0

# Plot the density map of the interferogram
I = pow(abs(transI), 0.5)
densityPlot(I, xAxis, yAxis, title, style,
            interpolation, saveDirectory, show)


#################### Power spectrum ##################################
'Define parameters'
# Number of pixels corresponding to 1 unit of real distance
dx = 1./(xPixel * (xRealDis/xPixel))
dy = 1./(yPixel * (yRealDis/yPixel))

# Set up lists of distance_to_pixel data
fxList = array([(i - xPixel/2. - 1) * dx for i in xrange(1, xPixel + 1)])
fyList = array([(i - yPixel/2. - 1) * dy for i in xrange(1, yPixel + 1)])

'Visualize phase peaks in the power spectrum at zero frequency'
# FFT data at zero frequency
zeroFFT = abs(transI[xPixel/2 - 1])
fxList = convert(fxList, 'mm')

# Set necessary parameters
title = r'The Power Spectrum of The Simulated Interferogram'
xtitle = r'X Distance (mm)'
ytitle = r'Intensity'
saveDirectory = "./results/step_03-power_spectrum_interferogram.jpg"
show = 0
gridlines = [convert(-fx0, 'mm'), convert(fx0, 'mm')]

# Plot the density map of the interferogram
xyPlot(fxList, zeroFFT, title, xtitle, ytitle,
       saveDirectory, show, gridlines)


############# Isolate the side-lobe for visualization ################
'Import the density image of the FFT of the interferogram'
filename = 'step_02-fft_interferogram.jpg'

'Find the centroids'
centroids = centroidSidelobe(filename)
object1 = [centroids[-1]]

'Isolate centroids that are belong to the left feature'
for i in xrange(len(centroids), 2, -1):
    if abs(centroids[i-2,0] - centroids[i-1,0]) < 20:
        object1.append(centroids[i-2])
    else:
        break

'Define the size of the scaled window for the side-lobe'
ydiff = abs(centroids[-1,1] - centroids[-4,1])/2 + 20
xdiff = ydiff

'Set the range of data used'
# Set the midpoint of the image
midPoint = xPixel/2
# Set the shift in x and y direction
yShift = ydiff*1.27
xShift = 0

'Isolate the side-lobe'
sidelobeWindow = deepcopy(transI[(midPoint + xShift) - xdiff : (midPoint + xShift) + xdiff]).T
sidelobeWindow = sidelobeWindow[(midPoint + yShift) - ydiff : (midPoint + yShift) + ydiff].T

'Visualize the isolated side-lobe'
# Set necessary parameters
title = r'Density Plot of The Side Lobe'
saveDirectory = "./results/step_04-sidelobe_density.jpg"
style = 'jet'
interpolation = 'gaussian'
show = 0

# Set up the axes size
xAxis = array([i for i in xrange(len(sidelobeWindow))])
yAxis = array([i for i in xrange(len(sidelobeWindow))])

'''
    The density plot of the side-lobe
'''

# Plot the density map of the side-lob
densityPlot(abs(sidelobeWindow), xAxis, yAxis, title, style, 
            interpolation, saveDirectory, show)

'''
    The power spectrum plot of the side-lobe
'''

# Set up the axes size
pixelWindow = abs(xShift - xdiff)
xAxis = array([i for i in xrange(len(sidelobeWindow[pixelWindow]))])

# Set necessary parameters
title = r'The Power Spectrum of The Simulated Side Lobe'
xtitle = r'X Distance (mm)'
ytitle = r'Intensity'
saveDirectory = "./results/step_05-power_spectrum_side_lobe.jpg"
show = 0
gridlines = [None, None]

# Plot the power spectrum of the side-lobe
xyPlot(xAxis, abs(sidelobeWindow[pixelWindow]), title, xtitle, ytitle,
       saveDirectory, show, gridlines)


############ Padding empty spaces in Fourier space ###################
'Pad the matrix with zeros in x and y directions'
sidelobeWindow = fixDim(sidelobeWindow, xPixel)


############# Perform the inverse Fourier transform ##################
'Perform the inverse Fourier transform'
invtransI = invFFT(sidelobeWindow, xPixel, xRealDis/xPixel)

'Plot the inverse FFT of the phase of the given interferogram'
# Set necessary parameters
title = r'The Inverse FFT of The Phase'
saveDirectory = "./results/step_06-inv_fft_interferogram.jpg"
style = 'Greys'
interpolation = 'gaussian'
show = 0

# Plot the density map of the phase
densityPlot(abs(invtransI), xAxis, yAxis, title, style,
            interpolation, saveDirectory, show)


################# Perform the phase extraction #######################
'Perform the phase extraction'
phaseProfile = phaseExtraction(invtransI)

'Plot the phase of the given interferogram'
# Set necessary parameters
title = r'Phase of The Interferogram'
saveDirectory = "./results/step_07-phase_interferogram.jpg"
style = 'jet'
interpolation = None
show = 0

# Plot the density map of the phase
densityPlot(phaseProfile, xAxis, yAxis, title, style,
            interpolation, saveDirectory, show)


##################### Image Enhancement ##############################
'Set the image folder'
folder = "case02-unknown_phase/results/"

'Increase the brightness of images'
enhancer(6, 1.3, folder)


#################### Perform the phase unwrap ########################


'''
    The threshold value is the tolerant gradient level between 2 adjacent
    data points. Try to vary it and observe the change.
'''


'Perform unwrapping of phase'
# Set the mode
mode = 0
# Set the threshold
threshold = 4.0
# Unwrap phase
phaseUnwrap = unwrapPhaseProfile(phaseProfile, mode, threshold)

'Plot the unwrapped phase of the given interferogram'
# Set necessary parameters
title = r'Unwrapped Phase of The Interferogram'
saveDirectory = "./results/step_08-unwrapped_phase_interferogram.jpg"
style = 'jet'
interpolation = None
show = 0

# Plot the density map of the phase
densityPlot(phaseUnwrap, xAxis, yAxis, title, style,
            interpolation, saveDirectory, show)

'Compare the unwrapped phase to the original one'
saveDirectory = "./results/step_09_compare-unwrapped_phase_interferogram.jpg"
# Plot the density map of the phase
densityPlot(realPhase, xAxis, yAxis, title, style,
            interpolation, saveDirectory, show)


##################### Examine the wavefront ##########################
'Plot the wavefront of the phase of the given interferogram'
# Set necessary parameters
title = r'Phase Wavefront of The Interferogram'
saveDirectory = "./results/step_10-phase_wavefront.jpg"
style = 'jet'
show = 0

# Plot the density map of the phase
surfacePlot(abs(phaseUnwrap), title, style,
            saveDirectory, show)
