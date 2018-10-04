from ij import IJ, ImagePlus, ImageStack
from ij.plugin.frame import RoiManager
from ij.plugin import Duplicator
from ij.plugin import ImageCalculator
from ij.plugin import ZProjector
from ij.measure import ResultsTable
import math
from java.awt import *
import itertools
from ij.gui import Roi
from ij.gui import PointRoi, OvalRoi
from java.lang import Boolean
import time
import itertools
import glob
import os
from ij.gui import WaitForUserDialog

from ij.plugin.filter import MaximumFinder
from ij.process import ImageProcessor
from ij import IJ, ImagePlus, ImageStack
from ij.gui import PointRoi
mf = MaximumFinder()
from ij.measure import Measurements
# Indicate channel which should be used for Thresholding

# Save the results automatically as  CSV file ?
automatic_save_results = True


do_dog_C1 = False
do_dog_C2 = False


savepath = "d://test3//SCR"


#path for CSV fave
#savepath = "d://test4//"+directory
#savepath = "d://test3//SCR"

# Clear all items from ROI manager
#rm = RoiManager.getInstance()
#rm.runCommand("reset")



roisize = 4

imp1 = IJ.getImage()

noise_C1 = 70
noise_C2 = 150

# def maxZprojection(stackimp):
#     """ from EMBL python / Fiji cookbook"""
#     allTimeFrames = Boolean.TRUE
#     zp = ZProjector(stackimp)
#     zp.setMethod(ZProjector.MAX_METHOD)
#     zp.doHyperStackProjection()
#     zpimp = zp.getProjection()
#     return zpimp


def DoG(imp0, kernel1, kernel2):
    """Thresholds image and returns thresholded image,
    merge code still quite clumsy but functional"""
    imp1 = imp0.duplicate()
    imp2 = imp0.duplicate()
    IJ.run(imp1, "Gaussian Blur...", "sigma=" + str(kernel1) + " stack")
    IJ.run(imp2, "Gaussian Blur...", "sigma="+ str(kernel2) + " stack")
    ic = ImageCalculator()
    imp3 = ic.run("Subtract create stack", imp1, imp2)
    return imp3


def ExtractChannel(imp, channel):
    imp_height = imp.getHeight()
    imp_width = imp.getWidth()
    channelnumber = imp.getNChannels()
    slicenumber = imp.getNSlices()
    timepoints = imp.getNFrames()
    ExtractedChannel = Duplicator().run(imp, channel, channel, 1, slicenumber, 1, timepoints)

    return ExtractedChannel


def ExtractTimpepointChannel(imp, channel, timepoint):
    imp_height = imp.getHeight()
    imp_width = imp.getWidth()
    channelnumber = imp.getNChannels()
    slicenumber = imp.getNSlices()
    ExtractedChannel = Duplicator().run(imp, channel, channel, 1, slicenumber, timepoint, timepoint)
    return ExtractedChannel

# identifying spots

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

timepoints = imp1.getNFrames()

ort = ResultsTable()
ort.setPrecision(3)

IJ.run(imp1, "Select All", "")
stats_all = imp1.getStatistics( Measurements.AREA)
print str(stats_all.area)
IJ.run(imp1, "Select None", "")


WaitForUserDialog("Select cell-free region","select background free of cells").show()             

stats_background = imp1.getStatistics( Measurements.AREA)
print str(stats_background.area)

IJ.run(imp1, "Select None", "")

for i in range (1, timepoints+1):
    IJ.run(imp1, "Select None", "")
    imp1.setT(i)
    # Extact channel to Threshold, set automatic threshold
    imp_threshold= ExtractTimpepointChannel(imp1, 1, i)

    if do_dog_C1:
        imp_DoG = DoG(imp_threshold,1,3)
    else:
        imp_DoG = imp_threshold
    #imp_DoG.show()
    #IJ.run(imp_DoG, "Z Project...", "projection=[Max Intensity] all")
    imp_DoG.setTitle("Difference_of_Gaussian")
    MeanChannel1 = []
    MeanChannel2= []
    maximaC1 = mf.getMaxima(imp_DoG.getProcessor(), noise_C1, True)
    #print maximaC1.npoints
    
    IJ.run(imp1, "Select None", "")
    imp1.setT(i)
    # Extact channel to Threshold, set automatic threshold
    imp_threshold= ExtractTimpepointChannel(imp1, 2, i)

    if do_dog_C2:
        imp_DoG = DoG(imp_threshold,1,3)
    else:
        imp_DoG = imp_threshold
    #imp_DoG.show()
    #IJ.run(imp_DoG, "Z Project...", "projection=[Max Intensity] all")
    imp_DoG.setTitle("Difference_of_Gaussian")
    MeanChannel1 = []
    MeanChannel2= []
    maximaC2 = mf.getMaxima(imp_DoG.getProcessor(), noise_C2, True)
    #print maximaC2.npoints




    imp_threshold.close()
    imp_DoG.close()
    ort.incrementCounter()
    ort.addValue("Frame", i)
    ort.addValue("Spots C1", maximaC1.npoints)
    ort.addValue("Spots C2", maximaC2.npoints)
    ort.addValue("Area occupied with cells in %", str((100-100/stats_all.area*stats_background.area)))
    ort.addValue("Area occupied with cells", str((stats_all.area-stats_background.area)))
    ort.addValue("Noise C1", str(noise_C1))
    ort.addValue("Noise C2", str(noise_C2))
    IJ.run(imp1, "Select None", "")

ort.show("Counted spots")

if automatic_save_results:
    dataname = imp1.getShortTitle()

    filename = dataname+".csv"
    #files = glob.glob(savepath+"/"+dataname+"*.csv")
    savename = savepath+"/"+filename
    ort.saveAs(savename)


"""
if automatic_save_results:
    dataname = imp1.getShortTitle()

    filename = dataname+"_001.csv"
    files = glob.glob(savepath+"/"+dataname+"*.csv")

    files.sort()
    #print files
    if len(files) == 0:
        cur_num = 0
    else:
        cur_num = int(os.path.basename(files[-1])[-7:-4])
        filename = os.path.basename(files[-1][:-7])
        cur_num +=1
        cur_num = str(cur_num).zfill(3)
        #print cur_num
        filename = filename+cur_num+str( os.path.basename(files[-1][-4:]))
    savename = savepath+"/"+filename
    ort.saveAs(savename)
"""