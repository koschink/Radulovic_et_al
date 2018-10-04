from ij import IJ
from ij import *
from ij import ImagePlus
from ij import ImageStack
from ij.measure import *
from ij.plugin import *
from ij.process import *
from ij.plugin import ChannelSplitter
from ij.measure import Measurements
from ij.plugin import ImageCalculator
from ij.plugin.frame import RoiManager
from ij.process import ImageProcessor
from ij.process import ImageStatistics
from ij.plugin import Duplicator
from ij.gui import Roi
from ij.gui import PointRoi
import math 
from java.awt import * 
from java.awt import Font
import itertools 
from ij.plugin.filter import MaximumFinder
from ij.measure import ResultsTable
from ij.gui import WaitForUserDialog


imp = IJ.getImage()

rm = RoiManager.getInstance()
rm.runCommand("reset")


def Duplicate(imp):
    imp_name = imp.getTitle()
    imp_height = imp.getHeight()
    imp_width = imp.getWidth()
    channelnumber = imp.getNChannels()
    slicenumber = imp.getNSlices()
    timepoints = imp.getNFrames()
    ExtractedChannel = Duplicator().run(imp, 1, channelnumber, 1, slicenumber, 1, timepoints)
    ExtractedChannel.setTitle("Duplicate_" + str(imp_name))
    return ExtractedChannel


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

imp_dup = Duplicate(imp)
imp_dup.show()
IJ.run(imp_dup, "Subtract Background...", "rolling=50 sliding stack");

imp_DoG1 = DoG(imp_dup,1,3)
imp_DoG1.show()
IJ.run("Threshold...")
# this is the method to wait the user set up the threshold
WaitForUserDialog("Threshold","set a threshold").show()    
thres_min = imp_DoG1.getProcessor().getMinThreshold()
thres_max = imp_DoG1.getProcessor().getMaxThreshold()
IJ.setThreshold(imp_DoG1, thres_min, thres_max);  
#IJ.run(imp_DoG1, "Convert to Mask", "");
IJ.run(imp, "Make Binary", "method=Default background=Default calculate black");
IJ.run("Set Measurements...", "area mean min center bounding stack");
IJ.run("Options...", "iterations=1 count=1 black do=Nothing");
IJ.run(imp_DoG1, "Analyze Particles...", "size=5-Infinity pixel display exclude clear summarize add stack");
