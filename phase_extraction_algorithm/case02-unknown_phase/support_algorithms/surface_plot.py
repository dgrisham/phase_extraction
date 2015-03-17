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
import numpy as np
from numpy import array
# Plotting
import matplotlib.pyplot as plt
import matplotlib as mp
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

'Import external Python modules'
# Set the modules' directory
import sys
sys.path.append("./")
# Import modules for unit conversion
from interferogram_simulation import convert


######################## Set up the graph ############################
'''
        The density plot 2D function. This general function is made as 
        generalized as possible to ensure minimal maintenance.
'''


def densityPlot(data, xAxis, yAxis, title, style, interpolation, save, show):
        # Set up the plot
        fig = plt.figure()

        # Set the title
        plt.title(title,
                          fontweight="bold", fontsize=14, color='black', fontstyle='italic')

        # Plot the density map
        plt.imshow(data,
                           extent=(xAxis[0]*1000, xAxis[-1]*1000, yAxis[0]*1000, yAxis[-1]*1000),
                   aspect='auto',
                   interpolation=interpolation,
                   cmap=style)

        # Add color bar to the plot for preference
        plt.colorbar()

        # Save image to the specified directory
        fig.patch.set_facecolor('white')
        plt.savefig(save,
                                facecolor=fig.get_facecolor(), edgecolor='none',
                bbox_inches=0, dpi=600)

        # Show the image
        if show == 1:
                plt.show()
                plt.close(fig)
        else:
                plt.close(fig)


'''
        The X-Y plot of data. It's used primarily for plotting the power 
        spectrum of the interferogram. It can also be used for any x-y plot.
'''


def xyPlot(xData, yData, title, xtitle, ytitle, save, show, gridlines):
        # Set up the plot
        fig = plt.figure()

        # Set the title
        plt.title(title,
                      fontweight="bold", fontsize=14, color='black', fontstyle='italic')

        # Label the x and y axis
        plt.xlabel(xtitle, fontweight="bold", fontsize=12, color='black')
        plt.ylabel(ytitle, fontweight="bold", fontsize=12, color='black')

        # Set axis limits
        plt.axis([xData[0], xData[-1], min(yData), max(yData) + 0.1*max(yData)])

        # Plot the X-Y map
        plt.plot(xData, yData,
                         color='red',
                         linestyle='-',
                         linewidth=2.
                         )

        # Display grid lines
        plt.grid()

        # Turn the grid on
        plt.axvline(x=0, ymin=-2, ymax=4, linestyle='-', color='blue', linewidth=.6)
        plt.axvline(x=gridlines[0], ymin=-2, ymax=4, linestyle='-', color='blue', linewidth=.6)
        plt.axvline(x=gridlines[1], ymin=-2, ymax=4, linestyle='-', color='blue', linewidth=.6)

        # Save image to the specified directory
        fig = plt.gcf()
        fig.patch.set_facecolor('white')
        plt.savefig(save,
                                facecolor=fig.get_facecolor(), edgecolor='none',
                bbox_inches=0, dpi=600)

        # Show the image
        if show == 1:
                plt.show()
                plt.close(fig)
        else:
                plt.close(fig)


'''
        The 3D surface plot of the wavefront constructed from the phase information.
'''


def surfacePlot(data, title, style, save, show):
        # Set up the plot
        fig = plt.figure()

        # Set up the axes size
        xAxis = array([i for i in xrange(len(data))])
        yAxis = array([i for i in xrange(len(data))])

        # Set up the X-Y coordinate axes
        xAxis, yAxis = np.meshgrid(xAxis, yAxis)

        # Plot the density map
        ax = fig.gca(projection='3d')
        surface = ax.plot_surface(xAxis, yAxis, data,
                                                          antialiased=False,
                                                          cmap=style)

        # Set the title
        ax.set_title(title,
                                 fontweight="bold", fontsize=20, 
                                 color='black', fontstyle='italic')

        # Set up the tick marks
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add color bar to the plot for preference
        fig.colorbar(surface, shrink=0.5, aspect=5)

        # Save image to the specified directory
        fig.patch.set_facecolor('white')
        plt.savefig(save,
                           facecolor=fig.get_facecolor(), edgecolor='none',
                           bbox_inches=0, dpi=600)

        # Show the image
        if show == 1:
                plt.show()
                plt.close(fig)
        else:
                plt.close(fig)
