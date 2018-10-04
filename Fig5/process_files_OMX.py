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
import matplotlib.ticker as ticker

import numpy
import glob
import random
import seaborn as sns
from scipy.stats import ttest_ind

from  matplotlib.ticker import FuncFormatter

datapath = "d:/maja/" 

dirnames = ["OMX"]


list1 = []

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 

pal = ["green","red"]

for dirnum,directory in enumerate(dirnames):
    print directory
    datapath1 = datapath+"/"+directory
    print datapath1
    files1 = glob.glob(datapath1+"/*.csv") 
    print files1 ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.')
        df1 = pd.DataFrame()
        df1["Spots"] = df["Spots C1"].copy()
        df1["normalized foci"] = df["Spots C1"]/(df["Area occupied with cells in %"]/100)
        df1["Channel"] = "Chmp4b"
        df1["seconds"]= df["Frame"].apply(lambda x:(x-1)/3)
        print "DF1 done"
        df2 = pd.DataFrame()
        df2["Spots"] = df["Spots C2"].copy()
        df2["normalized foci"] = df["Spots C2"]/(df["Area occupied with cells in %"]/100)
        df2["Channel"] = "Galectin3"
        df2["seconds"]= df["Frame"].apply(lambda x:(x-1)/3)
        df3 = pd.concat([df1, df2], axis=0)
        df3["Experiment"] = directory
        list1.append(df3)


dirnames = ["OMX2","OMX3"]


# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 

pal = ["green","red"]

for dirnum,directory in enumerate(dirnames):
    print directory
    datapath1 = datapath+"/"+directory
    print datapath1
    files1 = glob.glob(datapath1+"/*.csv") 
    print files1 ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.')
        df1 = pd.DataFrame()
        df1["Spots"] = df["Spots C1"].copy()
        df1["normalized foci"] = df["Spots C1"]/(df["Area occupied with cells in %"]/100)
        df1["Channel"] = "Galectin3"
        df1["min"]= df["Frame"].apply(lambda x:(x-1)/3)
        print "DF1 done"
        df2 = pd.DataFrame()
        df2["Spots"] = df["Spots C2"].copy()
        df2["normalized foci"] = df["Spots C2"]/(df["Area occupied with cells in %"]/100)
        df2["Channel"] = "Chmp4b"
        df2["min"]= df["Frame"].apply(lambda x:(x-1)/3)
        df3 = pd.concat([df1, df2], axis=0)
        df3["Experiment"] = directory
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

df4.reset_index(drop=True, inplace=True)
order1 = ["Chmp4b","Galectin3"]
g = sns.pointplot(x="min", y="normalized foci", hue="Channel", hue_order=order1, data=df4, ci=95, palette=pal)
    	
ticks = np.arange(0,61,3)

labels = np.arange(0,30,1)
g.set_xlabel("min")
g.set_ylabel("CHMP4B foci (normalized to cell area)")


#g.set_xticks(ticks)
#g.set_xticklabels(labels) # set the labels to display at those ticks
for index, label in enumerate(g.xaxis.get_ticklabels()):
    if index % 3 != 0:
        label.set_visible(False)

for index, label in enumerate(g.xaxis.get_ticklines()):
    if index % 3 != 0:
        label.set_visible(False)
g.xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x/3)))


condition1 = df4[df4["Channel"] == "Galectin3"]
condition2 = df4[df4["Channel"] == "Chmp4b"]
"""
p_values = []
for seconds in range (20, 1220,20):
    condition1_1 = condition1[condition1["seconds"] == seconds]
    condition2_1 = condition2[condition2["seconds"] == seconds]
    p_val = ttest_ind(condition1_1['normalized foci'], condition2_1['normalized foci'])
    p_values.append(p_val[1])

for item,value in enumerate(p_values):
    x_pos = item+1

    if value < 0.01:
        g.text(x_pos, 650, "*")
        print str(x_pos) + " significant"
    else:
        g.text(x_pos, 650, "-")
"""
plt.show()

               