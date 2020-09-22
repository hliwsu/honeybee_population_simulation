# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 20:10:55 2020

@author: haoli
"""

var_na = ["Date", "Colony Size", "Adult Drones", "Adult Workers", "Foragers", "Active Foragers", "Drone Brood", "Worker Brood",             "Drone Larvae", "Worker Larvae", "Drone Eggs", "Worker Eggs", "Total Eggs", "DD", "L", "N", "P", "dd",                "l", "n", "Free Mites", "Drone Brood Mites", "Worker Brood Mites", "Mites/Drone Cell", "Mites/Worker Cell", "Mites ying", "Proportion Mites Dying",                "Colony Pollen (g)", "Pollen Pesticide Concentration", "Colony Nectar", "Nectar Pesticide Concentration",                "Dead Drone Larvae", "Dead Worker Larvae", "Dead Drone Adults", "Dead Worker Adults", "Dead Foragers",                "Queen Strength", "Average Temperature (celsius)", "Rain", "Min Temp", "Max Temp", "Daylight hours", "Forage Inc", "Forage Day",                "New Worker Eggs", "New Drone Eggs", "Worker Eggs To Larvae", "Drone Eggs To Larvae", "Worker Larvae To Brood", "Drone Larvae To Brood", "Worker Brood To Adult", "Drone Brood To Adult",                 "Drone Adults Dying", "Foragers Killed By Pesticides", "Worker Adult To Foragers", "Winter Mortality Foragers Loss", "Foragers Dying"]

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
starting_clock = datetime.now()
print(starting_clock)
# =============================================================================
# obtain file names for the historical models
# =============================================================================
h_d=[]
for dirpath1, dirnames1, filenames1 in os.walk('Y:/Honeybee/data/historical/cold-storage-simulations-observed/Omak/observed'):
    for filename in [f for f in filenames1 ]:
        h_d.append(os.path.join(dirpath1, filename))
# =============================================================================
# obtain file names for the future models
# =============================================================================
f_d=[]
f_d_1=[] 
f_d_2=[] 
for dirpath, dirnames, filenames in os.walk('y:/Honeybee/data/future/cold-storage-results/Omak/rcp45'):
    for filename in [f for f in filenames ]:
        f_d.append(os.path.join(dirpath, filename))
    # obtain models
    for filename in [f for f in filenames if f.endswith("_default.txt")]:
        f_d_1.append(os.path.join(dirpath, filename))
    # obtain cold storage periods
    for filename in [f for f in filenames if f.startswith("bcc-csm1-1-m_cold_storage_")]:
        f_d_2.append(os.path.join(dirpath, filename))

# =============================================================================
# available models and codes
# BNU-ESM: 0
# CCSM4: 1 
# CNRM-CM5: 2
# CSIRO-Mk3-6-0: 3
# CanESM2: 4
# GFDL-ESM2G: 5
# GFDL-ESM2M: 6
# HadGEM2-CC365: 7
# HadGEM2-ES365: 8
# IPSL-CM5A-LR: 9
# IPSL-CM5A-MR: 10
# IPSL-CM5B-LR: 11
# MIROC-ESM-CHEM: 12
# MIROC5: 13
# MRI-CGCM3: 14
# NorESM1-M: 15
# bcc-csm1-1-m: 16
# bcc-csm1-1: 17
# inmcm4: 18
# =============================================================================


# =============================================================================
# available cold storage periods
# 09-15_02-15		0
# 09-15_02-22	: 	1
# 09-15_02-29	: 	2
# 09-15_03-01	: 	3
# 09-15_03-08	: 	4
# 09-15_03-15	: 	5
# 09-22_02-15	: 	6
# 09-22_02-22	: 	7
# 09-22_02-29	: 	8
# 09-22_03-01	: 	9
# 09-22_03-08	: 	10
# 09-22_03-15	: 	11
# 09-29_02-15	: 	12
# 09-29_02-22	: 	13
# 09-29_02-29	: 	14
# 09-29_03-01	: 	15
# 09-29_03-08	: 	16
# 09-29_03-15	: 	17
# 10-06_02-15	: 	18
# 10-06_02-22	: 	19
# 10-06_02-29	: 	20
# 10-06_03-01	: 	21
# 10-06_03-08	: 	22
# 10-06_03-15	: 	23
# 10-13_02-15	: 	24
# 10-13_02-22	: 	25
# 10-13_02-29	: 	26
# 10-13_03-01	: 	27
# 10-13_03-08	: 	28
# 10-13_03-15	: 	29
# 10-20_02-15	: 	30
# 10-20_02-22	: 	31
# 10-20_02-29	: 	32
# 10-20_03-01	: 	33
# 10-20_03-08	: 	34
# 10-20_03-15	: 	35
# no cold storage: 36 (for future use only)
# =============================================================================


        
# =============================================================================
# historical
# location-variable-coldstorage
# =============================================================================

# =============================================================================
# other inputs
# a. interested county (cnty)
# Omak=0; Richland=1; Walla Walla=2; Wenatchee=3
# b. if historical has cold storage (hist_cold)
# no = 0; yes = 1
# c. if future has cold storage (ftr_cold) 
# no = 0; yes = 1
# d. scenario (rcp)
# rcp45=0; rcp85=1
# e. future models (ftr_mdl)
# bcc-csm1-1_cold=0
# f. cold storage duration (csd)
# 36 options: 0-35
# =============================================================================

# =============================================================================
# obtain the path of historical data file
# =============================================================================
def hist_path(cnty, csd):
    if cnty==0:
        inter_mp='y:/Honeybee/data/historical/cold-storage-simulations-observed/Omak/observed/' # define intermediate path
    elif cnty==1:
        inter_mp='y:/Honeybee/data/historical/cold-storage-simulations-observed/Richland/observed/'
    elif cnty==2:
        inter_mp='y:/Honeybee/data/historical/cold-storage-simulations-observed/Walla Walla/observed/'
    elif cnty==3:
        inter_mp='y:/Honeybee/data/historical/cold-storage-simulations-observed/Wenatchee/observed/'        
    # if hist_cold==0:
    #     fl_hist="historical_default.txt"
    # if hist_cold==1:
    # fl_hist=hist_list[csd]
    hist_fl_path=inter_mp+filenames1[csd]
    return(hist_fl_path)
hist_path(1,35)
# =============================================================================
# obtain the path of future data file
# =============================================================================
def ftr_path(rcp, ftr_mdl, cnty, csd):
    if cnty==0:
        inter_mp='y:/Honeybee/data/future/cold-storage-results/Omak/'
    elif cnty==1:
        inter_mp='y:/Honeybee/data/future/cold-storage-results/Richland/'
    elif cnty==2:
        inter_mp='y:/Honeybee/data/future/cold-storage-results/Walla Walla/'
    elif cnty==3:
        inter_mp='y:/Honeybee/data/future/cold-storage-results/Wenatchee/'
    if rcp==0:
        rcp_mp="rcp45/"
    else:
        rcp_mp="rcp85/"
    mdl_ctrl=ftr_mdl*37 # corresponding to 19 models
    fl_seq=mdl_ctrl+csd
    print(fl_seq)
    ftr_fl_path=inter_mp+rcp_mp+filenames[fl_seq]
    return(ftr_fl_path)
ftr_path(0,1,2,3)
# =============================================================================
# v1=[]
# if v1: # if v1 has contents, then print
#     print("not empty")
# else:
#     print("empty list []")
# =============================================================================
def arg_check(v1,v2,v3,v4,v5,v6,v7):
    arg_list=[]
    if v1:
        arg_list.append(v1)
    if v2:
        arg_list.append(v2)
    if v3:
        arg_list.append(v3)
    if v4:
        arg_list.append(v4)   
    if v5:
        arg_list.append(v5)
    if v6:
        arg_list.append(v6)
    if v7:
        arg_list.append(v7)
    return(arg_list)
def data_reading(path,var0, var1=[], var2=[], var3=[], var4=[], var5=[], var6=[], var7=[]):
    var_list=arg_check(var1, var2, var3, var4, var5,var6,var7)
    var_list.insert(0,var0)
    var_all=arg_check(var1, var2, var3, var4, var5,var6,var7)
    var_all.insert(0,var0)
    var_all.insert(0,'Date')
    print(var_list)
    print(var_all)
    data = pd.read_csv(path, delim_whitespace=True, header=None, names=var_na, skiprows=6)
    data_df=data[var_all]
    return(var_list,var_all, data_df)
var_list,var_list_all,dataset1=data_reading('y:/Honeybee/data/historical/cold-storage-simulations-observed/Richland/observed/historical_cold_storage_10-20_03-15.txt', 'Forage Day','Forage Day','Forage Day','Forage Day','Forage Day','Forage Day','Forage Day','Forage Day')
import datetime as dt

# single data file, multiple vars plot
def sgl_fl_mlt_var_plots(hist, csd, cnty, var0, start,end, rcp=[],ftr_mdl=[],var1=[], var2=[], var3=[], var4=[], var5=[], var6=[], var7=[]): 
    if hist==1:
        path=hist_path(cnty, csd)
        a='12/31/1978'
    else:
        path=ftr_path(rcp, ftr_mdl, cnty, csd)
        a='12/31/2006'
    print(path)
    var_list,var_list_all, df=data_reading(path,var0, var1=var1, var2=var2, var3=var3, var4=var4, var5=var5, var6=var6, var7=var7)
    df['Date'][0]=a
    dates_list = [dt.datetime.strptime(date, '%m/%d/%Y').date() for date in df['Date']]
    df['dates']=    dates_list
    plot=df.plot(x='dates', y=var_list)
    plot.set_xlim(start, end)
    plt.gcf().set_size_inches(20, 10)
    print('hist'+str(hist)+str(var_list)+str(cnty)+".jpg")
    plt.savefig('hist'+str(hist)+str(var_list)+str(cnty)+".jpg")
    plt.close()
    return(var_list, df,dates_list)

# =============================================================================
# ### an alternative to resolve the figsize non-functioning issue is the following: ###
# def sgl_fl_sgl_asp_plots(hist, csd, cnty, var0, start,end, rcp=[],ftr_mdl=[],var1=[], var2=[], var3=[], var4=[], var5=[], var6=[], var7=[]): # single data file (single location), triple aspects plots
#     if hist==1:
#         path=hist_path(cnty, csd)
#     else:
#         path=ftr_path(rcp, ftr_mdl, cnty, csd)
#     var_list,var_list_all, df=data_reading(path,var0, var1=var1, var2=var2, var3=var3, var4=var4, var5=var5, var6=var6, var7=var7)
#     # df=enhance_data(df)
#     df['Date'][0]='12/31/1978'
#     dates_list = [dt.datetime.strptime(date, '%m/%d/%Y').date() for date in df['Date']]
#     df['dates']=    dates_list
#     fig = plt.figure(figsize=(30,15))
#     ax = fig.gca()
#     plot=df.plot(x='dates', y=var_list,ax=ax)
#     # plot.set_ylim(0, 20000)
#     plot.set_xlim(start, end)
#     # plot.axhline(2000.0, color="red", linestyle="--")
#     # plt.gcf().set_size_inches(20, 10)
#     plt.savefig("tmin_fl.jpg")
#     plt.close()
#     return(var_list, df,dates_list)
# =============================================================================

# a sample of historical data   
var_list,x,dl=sgl_fl_mlt_var_plots(hist=1,csd=2, cnty=2, var0="Adult Workers",start='01/02/1979', end='01/02/1985', var1="Colony Size", var2="Foragers Killed By Pesticides")
# a sample of future data
var_list,x,dl=sgl_fl_mlt_var_plots(hist=0,csd=2, cnty=2, var0="Adult Workers",start='01/02/2079', end='01/02/2085', rcp=0,ftr_mdl=2,var1="Colony Size", var2="Foragers Killed By Pesticides")
ending_clock = datetime.now()
print(ending_clock-starting_clock)
# i5-3610qm 12GB 0:00:20.919055


