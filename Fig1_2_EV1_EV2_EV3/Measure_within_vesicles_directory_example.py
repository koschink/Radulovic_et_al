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
from ij.plugin import Duplicator
from ij.process import ImageProcessor
from ij.process import ImageStatistics
from ij.gui import Roi
from ij.gui import PointRoi
import math 
from java.awt import * 
from java.awt import Font
import itertools 
from ij.plugin.filter import MaximumFinder
from ij.measure import ResultsTable
import time
from ij.gui import WaitForUserDialog
import os, errno
import glob
from ij.gui import Overlay

from ij.plugin import Concatenator

concat = Concatenator()

# Indicate channel which should be used for Thresholding

# Save the results automatically as  CSV file ?
automatic_save_results = True

#path for CSV fave
#savepath = "d:\Marte/EGF/"
draw_rois = True
threshold = [9000, 3577, 5000]
testmode = False

IJ.run("Set Measurements...", "median min mean stack redirect=None decimal=3");

#datapath = "D:/Eva/Maja/Experiment1/GFP-Vps36_Gal3/" 


datapath = "Example Directory structure"
dirnames = ["X","Y"]
savepath_base = datapath+"/Results/"

print savepath_base
channelnames = ["DAPI", "mChALIX", "Gal3", "Lamp1"]



# Clear all items from ROI manager
try:
    rm = RoiManager.getInstance()
    if rm.getCount() != 0:
        rm.runCommand("Delete");
except:
   rm = RoiManager()
   

Threshold_Channel = 4

measure_channels = [2,3,4]
nucleus_channel = 1

#imp1 = IJ.getImage()


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


def Generate_segmented_image(imp, channel):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()

    IJ.run(imp_Threshold_1, "Median...", "radius=1");
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.setAutoThreshold(imp_Threshold_1, "Moments dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1


def Segment_Nuclei(imp, channel):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Subtract...", "value=5000");
    IJ.run(imp_Threshold_1, "Median...", "radius=3");
    #IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=500");
    IJ.setAutoThreshold(imp_Threshold_1, "Li dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    IJ.run(imp_Threshold_1, "Erode", "");
    IJ.run(imp_Threshold_1, "Erode", "");
    IJ.run(imp_Threshold_1, "Erode", "");
    IJ.run(imp_Threshold_1, "Erode", "");
    IJ.run(imp_Threshold_1, "Erode", "");
    IJ.run(imp_Threshold_1, "Dilate", "");
    IJ.run(imp_Threshold_1, "Dilate", "");
    IJ.run(imp_Threshold_1, "Dilate", "");
    IJ.run(imp_Threshold_1, "Dilate", "");
    IJ.run(imp_Threshold_1, "Dilate", "");
    #IJ.run(imp_Threshold_1, "Dilate", "");    
    
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

def Generate_segmented_fixedThreshold(imp, channel, thres_min):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Median...", "radius=1");
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");

    IJ.setThreshold(imp_Threshold_1, thres_min, 100000);  
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1

for dirnum,directory in enumerate(dirnames):
    print directory
    datapath1 = datapath+"/"+directory
    files1 = glob.glob(datapath1+"/*ALX.dv")
    nuclei_count_sum = 0
    savepath = savepath_base+directory

     #Checking if savepath exists
    """
    try:
        os.makedirs(savepath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
       """

    for filenum, imagefile in enumerate(files1):
        print "Processing file #" + str(filenum) + " :" + str(imagefile)    
        if testmode:
            if filenum >5:
                print "Testmode active"
                print "stopping after" + str(filenum) + "files"
                break

       
        imp1 = IJ.openImage(imagefile)
        imp1 = IJ.getImage()



#        savepath = savepath_base+directory

        #Checking if savepath exists

#        try:
#            os.makedirs(savepath)
#       except OSError as e:
#           if e.errno != errno.EEXIST:
#               raise


        Nuclei = Segment_Nuclei(imp1, nucleus_channel)
        IJ.run(Nuclei, "Analyze Particles...", "size=5000-Infinity pixel circularity=0.3-1.00 add exclude stack");
        IJ.run("Tile", "");
        time.sleep(0.2)
        name1= imp1.getTitle()
        nuclei_count = rm.getCount()

        if rm.getCount() != 0:
            rois = rm.getIndexes()
            rm.setSelectedIndexes(rois);
            if rm.getCount() > 1: 
                rm.runCommand("Combine")
                rm.runCommand("Delete")
                rm.runCommand("Add")        
            rois1 = rm.getIndexes()
            for roi in rois1:
                rm.select(imp1, roi)
                imp1.setC(1)
                IJ.run(imp1, "Draw", "slice");
            
        IJ.selectWindow(name1)
        IJ.run("Select None");
            


        print nuclei_count
        nuclei_count_sum = nuclei_count_sum + nuclei_count
        if nuclei_count < 1:
            Nuclei.changes = False
            Nuclei.close()
            imp1.changes = False
            imp1.close()
            continue
        


        IJ.run("Clear Results", "");

        if rm.getCount() != 0:
            rm.runCommand("Delete");
        """           
        imp2 = Generate_segmented_image(imp1, Threshold_Channel)

        #imp2 = Generate_segmented_manual(imp1, Threshold_Channel, "Moments", 2)
        IJ.run(imp2, "Analyze Particles...", "size=15-Infinity pixel add exclude stack");
        IJ.run("Tile", "");
        time.sleep(0.2)
        """
        IJ.run("Clear Results", "");



        if rm.getCount() != 0:
            rm.runCommand("Deselect");
        for number, channel in enumerate(measure_channels):
            threshold_min = threshold[number]
            imp2 = Generate_segmented_fixedThreshold(imp1, channel, threshold_min)

            #imp2 = Generate_segmented_manual(imp1, Threshold_Channel, "Moments", 2)
            IJ.run(imp2, "Analyze Particles...", "size=15-500 pixel add exclude stack");
            IJ.run("Tile", "");
            #time.sleep(.2)
            
            imp1.setC(channel)
            
            #time.sleep(.2)
            rm.runCommand(imp1,"Measure");
            #time.sleep(.2)

            name1= imp1.getTitle()
            if draw_rois:            
                if rm.getCount() != 0:
                    rois = rm.getIndexes()
                    rm.setSelectedIndexes(rois);
                    if rm.getCount() > 1: 
                        rm.runCommand("Combine")
                        rm.runCommand("Delete")
                        rm.runCommand("Add")        
                    rois2 = rm.getIndexes()
                    for roi2 in rois2:
                        rm.select(imp1, roi2)
                        imp1.setC(channel)
                        print "Drawing"
                        IJ.run(imp1, "Draw", "slice");
                
            
            
            IJ.selectWindow(name1)
            IJ.run("Select None");
            if rm.getCount() != 0:
                rm.runCommand("Delete");
            imp2.changes = False
            imp2.close()
        ort = ResultsTable.getResultsTable()

        number_of_measurements = ort.getCounter()


    


        for i in range(0, number_of_measurements):
            results_channel = ort.getValue("Ch", i)
            
            channel_name = channelnames[int(results_channel)-1]
            ort.setValue("Channel", i, channel_name)
            ort.setValue("Nuclei", i, nuclei_count)
                    
            ort.updateResults()
        ort.show("Results")

        #time.sleep(2.5)
        Nuclei.changes = False
        Nuclei.close()
        imp2.changes = False
        imp2.close()

        if automatic_save_results:
            dataname = imp1.getTitle()
            filename = dataname+".csv"
            #files = glob.glob(savepath+"/"+dataname+"*.csv")
            savename = savepath+"/"+filename
            ort.saveAs(savename)
        else:
            print "not saving"
        
        if filenum == 0:
            dup = Duplicator()
            stack1 = dup.run(imp1)
            print "first round"
        else:
            try:
                dup = Duplicator()
                stack2 = dup.run(imp1)
                stack1 = concat.run(stack1, stack2)
                stack1.setTitle(directory)
                print "making stack"
            except NameError:
                dup = Duplicator()
                stack1 = dup.run(imp1)
                print "first image was empty"

        imp1.changes = False
        imp1.close()
        if rm.getCount() != 0:
            rm.runCommand("Delete");
        output_file = savepath+ "/nuclei_count.txt"
        with open(output_file, "w") as output:
            output.write(str(nuclei_count_sum)+ "\n")
    stack1.show()


"""
           
        for i, roi in enumerate(RoiManager.getInstance().getRoisAsArray()):
            rm.select(imp1, i)
            imp1.setC(2)
            stats2 = imp1.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
            imp1.setC(3)
            stats3 = imp1.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
            imp1.setC(4)
            stats4 = imp1.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
            ort.incrementCounter()
            ort.addValue("ROI", str(i))
            ort.addValue("Mean intensity Channel 2", str(stats2.mean))
            ort.addValue("Mean intensity Channel 3", str(stats3.mean))
            ort.addValue("Mean intensity Channel 4", str(stats4.mean))
            ort.addValue("Nuclei", str(nulei_count))


dataname = imp1.getShortTitle()
print dataname
filename_ort = "Measurements"+dataname+"_001.csv"
savename_ort = savepath+filename_ort # Generate complete savepath
print savename_ort
ort.saveAs(savename_ort) # save

rm.runCommand("reset")
# #####  Cleaning up... ####

# imp_DoG.changes = False
# imp_DoG.close()
# imp_DoG_zMax.changes = False
# imp_DoG_zMax.close()





    # # #    IJ.run(imp_measure, "Make Band...", "band=0.63")    # values are in um, assumes pixelsize of 0.21

    # #   # imp_measure.setRoi(roi)
    # #   # ROIFrame = roi.getPosition()
    # #   # imp_measure.setPosition(ROIFrame)
    # #  #    imp_measure.setT(roi.getTPosition())
    # #  #    imp_measure.setZ(roi.getZPosition())
    # #  #    imp_measure.setC(1)
    # #     IJ.run(imp_measure, "Measure", "")

    # dataname = imp1.getShortTitle()
    # ort = ResultsTable.getResultsTable()
    # if automatic_save_results:
    #     # Gather filenames of the savedirectory
    #     filename_ort = "Measurements_"+dataname+"_001.csv"
    #     files_ort = glob.glob(savepath+"/"+"Measurements_"+dataname+"*.csv")

    #     files_ort.sort() # sort by numbering, needed to get the last filenname number
    #     #print files
    #     # if len(files_ort) == 0: # check if a file exists, if not, simply use the existing filename
    #     #     cur_num_ort = 0  # do we need this?
    #     # else:
    #         # Check if filenames already exists, if so, get the last available number and increment by 1
    #     if len(files_ort) != 0:
    #         cur_num_ort = int(os.path.basename(files_ort[-1])[-7:-4]) # get the curtrent file number
    #         filename_ort = os.path.basename(files_ort[-1][:-7]) # get the current file name
    #         cur_num_ort += 1   # increment file number by 1
    #         cur_num_ort = str(cur_num_ort).zfill(3)  # pad it to 3 digits
    #         #print cur_num
    #         filename_ort = filename_ort+cur_num_ort+str(os.path.basename(files_ort[-1][-4:])) # generate final filename
    #     savename_ort = savepath+filename_ort # Generate complete savepath
    #     print savename_ort
    #     ort.saveAs(savename_ort) # save


"""
