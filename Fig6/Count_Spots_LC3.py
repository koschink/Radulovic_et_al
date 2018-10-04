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
import time

import os, errno
import glob

# Indicate channel which should be used for Thresholding

# Save the results automatically as  CSV file ?
automatic_save_results = True

#path for CSV save

datapath = "D:/Experiments/LC3/" 

dirnames = ["A","B","C","D"]

savepath_base = datapath+"/results/"

# Clear all items from ROI manager
rm = RoiManager.getInstance()
rm.runCommand("reset")

channel2_name = "Channel2"

channel3_name = "Channel3"

channel1_name = "Channel1"

channel4_name = "Channel4"




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
    ExtractedChannel.setTitle("Gallery_Channel_" + str(channel))
    return ExtractedChannel


def Generate_segmented(imp, channel, threshold_method, filtersize):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Median...", "radius="+str(filtersize));
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.setAutoThreshold(imp_Threshold_1, threshold_method+" dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1

def Generate_segmented_bgsub(imp, channel, threshold_method, filtersize):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Select All", "")
    stats = imp_Threshold_1.getStatistics(Measurements.MEAN |Measurements.STD_DEV )
    IJ.run(imp_Threshold_1, "Select None", "")
    background = stats.mean+ (2*stats.stdDev)
    IJ.run(imp_Threshold_1, "Subtract...", "value="+str(background));
    IJ.run(imp_Threshold_1, "Median...", "radius="+str(filtersize));
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.setAutoThreshold(imp_Threshold_1, threshold_method+" dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1

def Generate_segmented_DoG(imp, channel, threshold_method, filtersize):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    imp_Treshold_1 = DoG(imp_Threshold_1,2,4)
    #IJ.run(imp_Threshold_1, "Median...", "radius="+str(filtersize));
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.setAutoThreshold(imp_Threshold_1, threshold_method+" dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1

def Generate_segmented_manual(imp, channel, threshold_method, filtersize):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Median...", "radius="+str(filtersize));
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.run("Threshold...")
# this is the method to wait the user set up the threshold
    WaitForUserDialog("Threshold","set a threshold").show()    
    thres_min = imp_Threshold_1.getProcessor().getMinThreshold()
    thres_max = imp_Threshold_1.getProcessor().getMaxThreshold()
    IJ.setThreshold(imp_Threshold_1, thres_min, thres_max);  
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1



for dirnum,directory in enumerate(dirnames):
    print directory
    datapath1 = datapath+"/"+directory
    files1 = glob.glob(datapath1+"/*.lsm") 
    
    savepath = savepath_base+directory
    try:
        os.stat(savepath)
    except:
        os.mkdir(savepath) 

    for lsmfile in files1:
        imp1 = IJ.openImage(lsmfile)
        imp1.show()



        #Checking if savepath exists



        Channel1 = Generate_segmented(imp1, 1, "Li", 5)
        # # # # Generate ROIs by "Analyse Particles"

        IJ.run(Channel1, "Analyze Particles...", "size=100-Infinity pixel add exclude stack");
        IJ.run("Clear Results", "");

        Channel1_count = RoiManager.getInstance().getCount()
        print Channel1_count

        time.sleep(0.5)


        rm.runCommand("reset")



        Channel2 = Generate_segmented_manual(imp1, 2, "MaxEntropy", 1)
        # # # # Generate ROIs by "Analyse Particles"
        IJ.run(Channel2, "Analyze Particles...", "size=5-Infinity pixel add exclude stack");
        IJ.run("Clear Results", "");
        Channel2_count = RoiManager.getInstance().getCount()


        time.sleep(0.5)


        rm.runCommand("reset")

        Channel3 = Generate_segmented_manual(imp1, 3, "Moments", 2)

        # # # # Generate ROIs by "Analyse Particles"
        IJ.run(Channel3, "Analyze Particles...", "size=5-Infinity pixel add exclude stack");

        Channel3_count = RoiManager.getInstance().getCount()
        IJ.run("Clear Results", "");

        time.sleep(0.5)

        rm.runCommand("reset")

        Channel4 = Generate_segmented_manual(imp1, 4, "Moments", 2)
        # # # # Generate ROIs by "Analyse Particles"
        IJ.run(Channel4, "Analyze Particles...", "size=5-Infinity pixel add exclude stack");
        IJ.run("Clear Results", "");
        Channel4_count = RoiManager.getInstance().getCount()
        print Channel4_count
        time.sleep(0.5)


        rm.runCommand("reset")

        time.sleep(0.5)

        ort = ResultsTable() 
        ort.setPrecision(2)
        ort.incrementCounter()
        ort.addValue("Channel1", Channel1_count)
        ort.addValue("Channel2", Channel2_count)
        ort.addValue("Channel3", Channel3_count)
        ort.addValue("Channel4", Channel4_count)
        ort.show("Results")
        if automatic_save_results:
            dataname = imp1.getTitle()

            filename = dataname+".csv"
            #files = glob.glob(savepath+"/"+dataname+"*.csv")
            savename = savepath+"/"+filename
            ort.saveAs(savename)

        Channel1.changes = False
        Channel1.close()
        Channel2.changes = False
        Channel2.close()
        Channel3.changes = False
        Channel3.close()
        Channel4.changes = False
        Channel4.close()
        imp1.close()


