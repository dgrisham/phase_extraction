'''
    Collaborators: Lam H. Mach & David Grisham
    Engineering Physics 2016
    Date: 02/26/2015
    Faculty Adviser: Dr. Charles Durfee
    Department of Physics
    Colorado School of Mines
'''


################# Import modules and Python packages #################
# Computation
from numpy import array, angle
import numpy as np
from copy import deepcopy
# Image processing
from PIL import Image, ImageEnhance
# OpenCV for Computer vision
import cv2
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
images = array(["step_01-interferogram.jpg",
                                "step_02-fft_interferogram.jpg",
                                "step_03-power_spectrum_interferogram.jpg",
                                "step_04-sidelob_density.jpg",
                                "step_05-power_spectrum_side_lob.jpg",
                                "step_06-invfft_interferogram.jpg",
                                "step_07-phase_interferogram.jpg",
                                "step_08-unwrapped_phase_interferogram.jpg",
                                "step_09_compare-unwrapped_phase_interferogram.jpg",
                                "step_10-phase_wavefront.jpg"
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
        path = os.path.abspath(os.path.join(os.getcwd(),os.pardir)) + "/" + folder
        # Input the image
        I, path = imageIn(image, path)

        # Pass the image to the ImageEnhance function in Image package
        enhance = ImageEnhance.Brightness(I)

        # Pass the new brightness to the image
        brighterImage = enhance.enhance(brightness)

        # Return the newly enhanced image
        brighterImage.save(path)


##################### Tracking the side lobes ########################


'''
        The blob around each side lobe is detected by using OpenCV Computer
        vision package. More information can be found in OpenCV website.
        For documentation, please visit this address:
                1) http://docs.opencv.org/trunk/doc/py_tutorials/py_tutorials.html
        For installation instruction, go to this website:
                2) http://docs.opencv.org/trunk/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
'''


'Track the centroid of the side lobes'
def centroidSidelobe(imageName):
        # Import the image
        image = cv2.imread("./results/" + imageName)

        # Check dimensions of image (width, height)
        imageDim = Image.open("./results/" + imageName).size
        width = imageDim[0]
        height = imageDim[1]
        
        # Adjust the kernel before performing dilation algorithm on the image
        kernel = np.ones((5, 5), np.uint8)

        # Image dilation
        image = cv2.dilate(image, kernel, iterations = 1)

        # Convert to gray-scaled image
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Define the threshold level
        ret,thresh = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

        # Find the contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Generate all centroids
        print "Number of centroids detected: ", len(contours)
        centroids = array([[0,0]])

        # Selection of centroids
        for i in contours:
                # Contour information
                centArea = cv2.contourArea(i)                           # Area
                centMoments = cv2.moments(i)                            # Moments
                centPerimeter = cv2.arcLength(i, True)          # Perimeter

                # Rectangular box (Square box)
                x, y, w, h = cv2.boundingRect(i)
                
                # Only accept detections near the center of the image
                if x > width/2 - 500 and x < width/2 + 200:
                        if y > height/2 - 200 and y < height/2 + 200: 
                                # Generate square box
                                if w > h:
                                        # Set width equal to height
                                        h = w
                                        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)

                                else:
                                        # Set width equal to height
                                        w = h
                                        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
                                
                                # Write blobs to the image file
                                cv2.imwrite("./results/blob_detection.jpg", image)

                                # Save centroids to array
                                centroids = np.append(centroids, [[x, y]], axis=0)
                        else:
                                continue
                else:
                        continue

        # Delete the first element since it's (0, 0)
        centroids = deepcopy(np.delete(centroids, (0), 0))

        # Return contour's information
        return sort(centroids, 0)

'Rank array'
def sort(vector, axis):
        # Set parameters
        change = 1

        # Rank algorithm
        while change != 0:
                # Reset the change for every iteration
                change = 0

                # Sorting
                for i in xrange(1, len(vector)):
                        # Assign values
                        a = deepcopy(vector[i-1])
                        b = deepcopy(vector[i])

                        # Wrong order
                        if vector[i-1, axis] > vector[i, axis]:
                                vector[i-1] = b
                                vector[i] = a
                                change += 1
                        
                        # Right order
                        else:
                                continue

        # Return the sorted vector
        return vector
