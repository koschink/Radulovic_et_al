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
plt.rcParams["figure.figsize"] = (12,6)


datapath = "D:/Experiments/LC3/Results" 

dirnames = ["A","B","C","D"]
timepoints = [0, 5,10,15,30,60,120]

list1 = []

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 


for dirnum,directory in enumerate(dirnames):
    print (directory)
    datapath1 = datapath+"/"+directory
    print (datapath1)
    files1 = glob.glob(datapath1+"/*.csv") 
    print (files1) ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.')
        df1 = pd.DataFrame()
        df1["Foci"] = df["Channel1"].copy()
        df1["Channel"] = "Nucleus"
        df1["Timepoint after LLOMe treatment"] = directory
        df1["Timepoint (min)"] = timepoints[dirnum]
        df1["Image"] = str(filenum)
        df2 = pd.DataFrame()
        df2["Foci"] = df["Channel2"].copy()
        df2["Foci per cell"]= df["Channel2"]/df["Channel1"]
        df2["Channel"] = "Chmp4b"
        df2["Timepoint after LLOMe treatment"] = directory
        df2["Timepoint (min)"] = timepoints[dirnum]
        df2["Image"] = str(filenum)
        df3 = pd.DataFrame()
        df3["Foci"] = df["Channel3"].copy()
        df3["Foci per cell"]= df["Channel3"]/df["Channel1"]
        df3["Channel"] = "Gal3"
        df3["Timepoint after LLOMe treatment"] = directory
        df3["Timepoint (min)"] = timepoints[dirnum]
        df3["Image"] = str(filenum)
        df4 = pd.DataFrame()
        df4["Foci"] = df["Channel4"].copy()
        df4["Foci per cell"]= df["Channel4"]/df["Channel1"]
        df4["Channel"] = "LC3"
        df4["Timepoint after LLOMe treatment"] = directory
        df4["Timepoint (min)"] = timepoints[dirnum]
        df4["Image"] = str(filenum)

        df3 = pd.concat([df1, df2, df3, df4], axis=0)


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

df5 = df4[df4["Channel"] != "Nucleus"]

f, ax = plt.subplots()

flatui = ["gray", "gray"]
pal1 = ["gray", "gray", "gray"]

g = sns.pointplot(x="Timepoint after LLOMe treatment", y="Foci per cell", hue="Channel", data=df5, join=False, capsize=.1, alpha=1, markers="_", ci=95, dodge=False  )
#g = sns.boxplot(x="Timepoint after LLOMe treatment", y="Foci per cell", hue="Channel", data=df5, dodge=True)

g = sns.swarmplot(x="Timepoint after LLOMe treatment", y="Foci per cell", hue="Channel", data=df5, dodge=False, size=5)


"""
g = sns.pointplot(x="Timepoint", y="Spots", hue="Channel", data=df4)
g = sns.stripplot(x="Timepoint", y="Spots", hue="Channel", dodge=False, alpha=1, data=df4, size=7) #,  palette=flatui
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[:2], labels[:2], title="number of spots",
          handletextpad=0, columnspacing=1,
          loc="upper left", ncol=2, frameon=True)
"""
plt.show()


j = sns.FacetGrid(df5, col="Channel", hue="Channel", sharey=False, size=5, aspect=0.9)
j.map(sns.pointplot, "Timepoint after LLOMe treatment", "Foci per cell", data=df5, join=False, ci=95, capsize=.1)
j.map(sns.swarmplot, "Timepoint after LLOMe treatment", "Foci per cell", data=df5, size=5)
#g.set(xticks=[10, 30, 50, 70, 90, 110], xticklabels=[10, 30, 50, 70, 90, 110])
