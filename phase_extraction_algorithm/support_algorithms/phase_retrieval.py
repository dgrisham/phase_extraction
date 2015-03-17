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
from numpy import array, angle, arctan2, pi, concatenate, append
import numpy as np
from math import copysign
from copy import deepcopy


'''
	Calculate the phase angle in the complex plane as well as unwrapping 
	phase. The objective is to select the right radian section in the unit 
	circle for each phase of the interferogram.
'''


##################### Perform the phase extraction ###################
'Perform the phase extraction'
def phaseExtraction(data):
	# Find the phase angle in the complex plane
	for i in xrange(len(data)):
		for j in xrange(len(data)):
			data[i, j] = arctan2(data[i, j].imag, data[i, j].real)

	# Return the results
	return data.real


'''
	There are 3 ways one can do to unwrap the phase. We simply call 
	them 3 modes. 
		a) The first mode (-1) unwraps the phase from left to right.
		b) The second mode (+1) unwraps the phase from right to left.
		c) The last mode (0) unwraps the phase from the center.
	Although these modes have different starting points, the procedure 
	associated with each mode remains the same.

	The Numpy unwrap function in Python doesn't seem to work. Further 
	testing is required to confirm this.
'''


######################## Perform the phase unwrap ####################
'Unwrap procedure / algorithm'
def unwrapAlgorithm(data, mode, gradient):
	# Define parameters and constants
	'Set the x-range correctly for each mode'
	if mode == 0:
		xRange = len(data) - 1
	else:
		xRange = len(data)
	
	unwrap = array([0. for i in xrange(xRange)])
	tmp = 0.

	'''
		The threshold level is predetermined. It's based on the angle
		of the incoming waves' electric fields.
	'''

	# Set phase shift and threshold
	phaseShift = 0.
	threshold = gradient

	'''
		The edge value is essentially ignored for all modes
	'''

	# Set initial values
	unwrap[0] = data[0]

	# Unwrap algorithm
	for i in xrange(1, xRange):
		# Compute the gradient between 2 adjacent points
		tmp = data[i-1] - data[i]

		# If the difference is greater than the assigned threshold, adjust the phase
		if abs(tmp) > threshold:
			phaseShift += copysign(2.*pi, tmp)

		# Shift the phase
		unwrap[i] = data[i] + phaseShift

	'''
		Since we shifted the data earlier for mode 1, we have to shift 
		the data back to the original arrangement.
	'''

	# Return the unwrapped phase
	if mode == -1 or mode == 0:
		return unwrap
	else:
		return unwrap[::-1]

'Unwrap one single phase'
def unwrapPhase(data, mode, xPixel, gradientThres):
	# Unwrap the phase
	'Mode 1: Unwrap left to right (Simplest)'
	if mode == -1:
		unwrap = unwrapAlgorithm(data, mode, gradientThres)

	'Mode 2: Unwrap right to left (Notice the data is reverse-ordered)'
	if mode == 1:
		unwrap = unwrapAlgorithm(data[::-1], mode, gradientThres)

	'Mode 3: Unwrap from the center (A little tricky)'
	if mode == 0:
		# Split the unwrapping process
		center = data[xPixel/2]
		center_left = unwrapAlgorithm(data[:xPixel/2+1][::-1], mode, gradientThres)
		center_right = unwrapAlgorithm(data[xPixel/2::], mode, gradientThres)

		# Combine the results
		unwrap = append(append(center_left[::-1], center), center_right)

	# Return the unwrapped phase
	return unwrap

'Unwrap multiple phases'
def unwrapPhaseProfile(phaseData, mode, gradientThres):
	# Define parameters and constants
	xPixel = len(phaseData)

	# Prepare lists for unwrapped phases
	unwrapXY = array([[0. for i in xrange(xPixel)]] * xPixel)
	unwrapYX = array([[0. for i in xrange(xPixel)]] * xPixel)

	# Loop through the N x N matrix and unwrap the phase of each row
	for i in xrange(xPixel):
		unwrapXY[i,::] = unwrapPhase(phaseData[i], mode, xPixel, gradientThres)

	'''
		The code above only unwraps the phase profile in the X direction
		(between columns). Next, we will unwrap the phase profile in the 
		Y direction (between rows).
	'''

	# Transpose the unwrapXY matrix to the unwrapYX matrix
	temporaryMatrix = deepcopy(unwrapXY.T)

	# Loop through the N x N matrix and unwrap the phase of each row	
	for i in xrange(xPixel):
		unwrapYX[i,::] = unwrapPhase(temporaryMatrix[i], mode, xPixel, gradientThres)

	# Transpose back to the original matrix
	unwrapXY = deepcopy(unwrapYX.T)

	# Return the unwrapped phase profile
	return unwrapXY