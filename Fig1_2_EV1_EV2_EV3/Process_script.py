# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 08:50:37 2018

@author: kaysch
"""
from __future__ import print_function
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
plt.rcParams["figure.figsize"] = (12,8)



list1 = []

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 



#df3 = df2.query("Channel == 2")
#fig = plt.figure(1)
#ax1 = fig.add_subplot(111)
#df3["Count"] = df3.groupby("Cell")["Point #"].transform('count')
#df3["Mean_Int_Norm"] = ((df3["Mean Intensity of spot"] - df3["Mean Intensity of spot"].min()) / (df3["Mean Intensity of spot"].max() - df3["Mean Intensity of spot"].min())*100)
#sns.violinplot(df3["Mean_Int_Norm"], df3.Count, color="cubehelix", bw="silverman",inner="box")
#ax1.set_xlabel("Number of spots per cell")
#ax1.set_ylabel("Mean intensity per Spot")
#sns.despine()


#datapath = "I:/780/02_05_18/XBP1u_in_KO/results/" 
datapath = "Data path/Results"

dirnames = ["X", "Y"]
channelnames = ["a", "b", "c", "d"]

palette3 = ["Magenta", "Cyan"]

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
        df["Treatment"] = directory
        df["Image"] = str(filenum)
        
        



        list1.append(df)
        



df4 = pd.concat(list1, axis=0)

f, ax = plt.subplots()

flatui = ["gray", "gray"]

g = sns.boxplot(x="Channel", y="Max", hue="Treatment", data=df4[df4["Ch"] == 2], dodge=True, palette=palette3)
plt.show()
g = sns.boxplot(x="Channel", y="Max", hue="Treatment", data=df4[df4["Ch"] == 3], dodge=True, palette=palette3)
plt.show()

#plt.ylim(0, 600)
"""
g = sns.pointplot(x="Timepoint", y="Spots", hue="Channel", data=df4)
g = sns.stripplot(x="Timepoint", y="Spots", hue="Channel", dodge=False, alpha=1, data=df4, size=7) #,  palette=flatui
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[:2], labels[:2], title="number of spots",
          handletextpad=0, columnspacing=1,
          loc="upper left", ncol=2, frameon=True)
"""
plt.show()


g = sns.boxplot(x="Channel", y="Mean", hue="Treatment", data=df4[df4["Ch"] == 2], dodge=True, palette=palette3)
plt.show()
g = sns.boxplot(x="Channel", y="Mean", hue="Treatment", data=df4[df4["Ch"] == 3], dodge=True, palette=palette3)
plt.show()


#plt.ylim(0, 600)
"""
g = sns.pointplot(x="Timepoint", y="Spots", hue="Channel", data=df4)
g = sns.stripplot(x="Timepoint", y="Spots", hue="Channel", dodge=False, alpha=1, data=df4, size=7) #,  palette=flatui
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[:2], labels[:2], title="number of spots",
          handletextpad=0, columnspacing=1,
          loc="upper left", ncol=2, frameon=True)
"""
plt.show()

savename = datapath + "Resultstable.xls"
results_table = df4.groupby(["Channel", "Treatment"]).describe()["Mean"]
results_table.to_excel(savename)
#g.set(xticks=[10, 30, 50, 70, 90, 110], xticklabels=[10, 30, 50, 70, 90, 110])
