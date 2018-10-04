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


from ij.plugin.filter import MaximumFinder
from ij.process import ImageProcessor
from ij import IJ, ImagePlus, ImageStack
from ij.gui import PointRoi
mf = MaximumFinder()
from ij.measure import Measurements
# Indicate channel which should be used for Thresholding

# Save the results automatically as  CSV file ?
automatic_save_results = True


datapath = "D:/Manuscript_2018/20180605_REVISION/Fig4/data2"
dirnames = ["0","10minLLOMe","30minLLOMe","60minLLOMe"]


do_dog_C1 = False
do_dog_C2 = False

roisize = 4


noise_C1 = 90
noise_C2 = 150

rm = RoiManager.getInstance()
rm.runCommand("reset")

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



for dirnum,directory in enumerate(dirnames):
    print directory
    datapath1 = datapath+"/"+directory
    files1 = glob.glob(datapath1+"/*.lsm") 
    for lsmfile in files1:
        imp1 = IJ.openImage(lsmfile)
        imp1.show()
        
        
        savepath = datapath +"/results/"+directory

        timepoints = imp1.getNFrames()

        ort = ResultsTable()
        ort.setPrecision(3)

        for i in range (1, timepoints+1):
            IJ.run(imp1, "Select None", "")
            imp1.setT(i)
            

            Channel1 = Generate_segmented(imp1, 1, "Li", 5)
        # # # # Generate ROIs by "Analyse Particles"

            IJ.run(Channel1, "Analyze Particles...", "size=100-Infinity pixel add stack");
            IJ.run("Clear Results", "");

            Channel1_count = RoiManager.getInstance().getCount()
            print Channel1_count

            time.sleep(0.5)
            Channel1.changes=False
            Channel1.close()

            rm.runCommand("reset")

            
            # Extact channel to Threshold, set automatic threshold
            imp_threshold= ExtractTimpepointChannel(imp1, 2, i)

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
            print maximaC1.npoints
            
            IJ.run(imp1, "Select None", "")
            imp1.setT(i)
            # Extact channel to Threshold, set automatic threshold
            imp_threshold= ExtractTimpepointChannel(imp1, 3, i)

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
            print maximaC2.npoints




            imp_threshold.close()
            imp_DoG.close()
            ort.incrementCounter()
            ort.addValue("Frame", i)
            ort.addValue("Cells", Channel1_count)
            ort.addValue("Spots C1", maximaC1.npoints)
            ort.addValue("Spots C2", maximaC2.npoints)
            IJ.run(imp1, "Select None", "")

        ort.show("Counted spots")

        if automatic_save_results:
            dataname = imp1.getTitle()

            filename = dataname+".csv"
            #files = glob.glob(savepath+"/"+dataname+"*.csv")
            savename = savepath+"/"+filename
            ort.saveAs(savename)
        imp1.changes=False
        imp1.close()


