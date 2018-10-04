# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 08:50:37 2018

@author: kaysch
"""

from __future__ import division
from pandas import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import numpy
import glob
import random
import seaborn as sns
import matplotlib.ticker as ticker


datapath = "D:/Experiments/DeltaVision/Fig4B_E108_LysoTrackerKDs/Quantifications for the paper_normalized to area/doubleKDs" 

dirnames = [ "siCtrl","siTsg101siAlix"]
list1 = []

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 


for dirnum,directory in enumerate(dirnames):
    print(directory)
    datapath1 = datapath+"/"+directory
    print(datapath1)
    files1 = glob.glob(datapath1+"/*.csv") 
    print(files1) ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.', index_col=0)
        df1 = pd.DataFrame()
        df1["Spots"] = df["Spots C1"].copy()
        df1["normalized Spots"] = df["Spots C1"]/(df["Area occupied with cells in %"]/100)
        df1["Channel"] = "Chmp4B"
        df1["Timepoint"] = df["Frame"]
        df1["Treatment"] = directory
        df1["Image"] = str(filenum+1)
        df2 = pd.DataFrame()
        df2["Spots"] = df["Spots C2"].copy()
        df2["normalized Spots"] = df["Spots C2"]/(df["Area occupied with cells in %"]/100)
        df2["Channel"] = "Lysotracker"
        df2["Timepoint"] = df["Frame"]
        df2["Treatment"] = directory
        df2["Image"] = str(filenum+1)
        df3 = pd.concat([df1, df2], axis=0)


        list1.append(df3)



#df3 = df2.query("Channel == 2")
#fig = plt.figure(1)
#ax1 = fig.add_subplot(111)
#df3["Count"] = df3.groupby("Cell")["Point #"].transform('count')
#df3["Mean_Int_Norm"] = ((df3["Mean Intensity of spot"] - df3["Mean Intensity of spot"].min()) / (df3["Mean Intensity of spot"].max() - df3["Mean Intensity of spot"].min())*100)
#sns.violinplot(df3["Mean_Int_Norm"], df3.Count, color="cubehelix", bw="silverman",inner="box")
#ax1.set_xlabel("Number of spots per cell")
#ax1.set_ylabel("Mean intensity per Spot")
#sns.despine()


df4 = pd.concat(list1, axis=0)

fig, ax = plt.subplots(figsize=(15,12))
g = sns.pointplot(x="Timepoint", y="normalized Spots", hue="Treatment", data=df4[df4["Channel"]=="Lysotracker"],ci=95,)
#g = sns.pointplot(x="Timepoint", y="Spots", hue="Genotype", data=df4[df4["Channel"]=="Lysotracker"], ci=None, palette="Blues")
g.xaxis.set_major_locator(ticker.MultipleLocator(10))
g.xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.show()
fig, ax = plt.subplots(figsize=(15,12))
g = sns.pointplot(x="Timepoint", y="normalized Spots", hue="Treatment", data=df4[df4["Channel"]=="Chmp4B"])

g.xaxis.set_major_locator(ticker.MultipleLocator(10))
g.xaxis.set_major_formatter(ticker.ScalarFormatter())
#g = sns.swarmplot(x="Timepoint", y="normalized Spots", data=df4, hue="Channel")

#g.set(xticks=[10, 30, 50, 70, 90, 110], xticklabels=[10, 30, 50, 70, 90, 110])
