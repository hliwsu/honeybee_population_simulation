# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 23:24:48 2020

@author: haoli

state 2, second revision
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import datetime as dt
from varname import nameof
import simplejson
starting_clock = datetime.now()
print(starting_clock)
var_na = ["Date", "Colony Size", "Adult Drones", "Adult Workers", "Foragers", "Active Foragers", "Drone Brood", "Worker Brood",             "Drone Larvae", "Worker Larvae", "Drone Eggs", "Worker Eggs", "Total Eggs", "DD", "L", "N", "P", "dd",                "l", "n", "Free Mites", "Drone Brood Mites", "Worker Brood Mites", "Mites/Drone Cell", "Mites/Worker Cell", "Mites ying", "Proportion Mites Dying",                "Colony Pollen (g)", "Pollen Pesticide Concentration", "Colony Nectar", "Nectar Pesticide Concentration",                "Dead Drone Larvae", "Dead Worker Larvae", "Dead Drone Adults", "Dead Worker Adults", "Dead Foragers",                "Queen Strength", "Average Temperature (celsius)", "Rain", "Min Temp", "Max Temp", "Daylight hours", "Forage Inc", "Forage Day",                "New Worker Eggs", "New Drone Eggs", "Worker Eggs To Larvae", "Drone Eggs To Larvae", "Worker Larvae To Brood", "Drone Larvae To Brood", "Worker Brood To Adult", "Drone Brood To Adult",                 "Drone Adults Dying", "Foragers Killed By Pesticides", "Worker Adult To Foragers", "Winter Mortality Foragers Loss", "Foragers Dying"]
future_model_list=["BNU-ESM","CCSM4","CNRM-CM5","CSIRO-Mk3-6-0","CanESM2","GFDL-ESM2G","GFDL-ESM2M","HadGEM2-CC365","HadGEM2-ES365","IPSL-CM5A-LR","IPSL-CM5A-MR","IPSL-CM5B-LR","MIROC-ESM-CHEM","MIROC5","MRI-CGCM3","NorESM1-M","bcc-csm1-1-m","bcc-csm1-1","inmcm4"]
cold_storage_period_list=["09-15_02-15","09-15_02-22","09-15_02-29","09-15_03-01","09-15_03-08","09-15_03-15","09-22_02-15","09-22_02-22","09-22_02-29","09-22_03-01","09-22_03-08","09-22_03-15","09-29_02-15","09-29_02-22","09-29_02-29","09-29_03-01","09-29_03-08","09-29_03-15","10-06_02-15","10-06_02-22","10-06_02-29","10-06_03-01","10-06_03-08","10-06_03-15","10-13_02-15","10-13_02-22","10-13_02-29","10-13_03-01","10-13_03-08","10-13_03-15","10-20_02-15","10-20_02-22","10-20_02-29","10-20_03-01","10-20_03-08","10-20_03-15","no cold storage"]
county_list=["Omak",'Richland','Walla Walla','Wenatchee']
rcp_list=["rcp45","rcp85"]
endash='_cold_storage_'
suffix='.txt'
fixed_hist_path='D:/Honeybee/data/historical/cold-storage-simulations-observed/'
fixed_future_path='D:/Honeybee/data/future/cold-storage-results/'
# =============================================================================
# file path module
# =============================================================================
# historical file path
def hist_path(cnty, csd_h):
    if csd_h==36:
        hist_fl_path=fixed_hist_path+county_list[cnty]+'/observed/historical_default.txt'
    else:
        hist_fl_path=fixed_hist_path+county_list[cnty]+'/observed/historical_cold_storage_'+cold_storage_period_list[csd_h]+suffix
    return(hist_fl_path)
# Walla Walla, 10-13_03-08
# hist_path(2,36)
# future file path
def ftr_path(rcp, ftr_mdl, cnty, csd_f):
    if csd_f==36:
        ftr_fl_path=fixed_future_path+county_list[cnty]+'/'+rcp_list[rcp]+'/'+future_model_list[ftr_mdl]+'_default.txt'
    else:
        ftr_fl_path=fixed_future_path+county_list[cnty]+'/'+rcp_list[rcp]+'/'+future_model_list[ftr_mdl]+endash+cold_storage_period_list[csd_f]+suffix
    return(ftr_fl_path)
# =============================================================================
# Variable option module
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
# =============================================================================
# Data reading module
# =============================================================================
def data_reading(path,var0, var1=[], var2=[], var3=[], var4=[], var5=[], var6=[], var7=[]):
    var_list=arg_check(var1, var2, var3, var4, var5,var6,var7)
    var_list.insert(0,var0)
    var_all=arg_check(var1, var2, var3, var4, var5,var6,var7)
    var_all.insert(0,var0)
    var_all.insert(0,'Date')
    data = pd.read_csv(path, delim_whitespace=True, header=None, names=var_na, skiprows=6)
    data_df=data[var_all]
    return(var_list,var_all, data_df)
# =============================================================================
# Difference in difference (DiD) data preparation
# =============================================================================
format='%m/%d/%Y'
def did_prep(treatment_cnty, control_cnty, rcp, ftr_mdl, did_var,csd_h,csd_f):
    hist_tr_path=hist_path(treatment_cnty, 36)
    hist_ct_path=hist_path(control_cnty, 36)
    ftr_tr_path=ftr_path(rcp, ftr_mdl, treatment_cnty, csd_f=csd_f)
    ftr_ct_path=ftr_path(rcp, ftr_mdl, control_cnty, csd_f=36) # yes, use csd_f=36
    fl_phs=[ hist_tr_path , hist_ct_path , ftr_tr_path , ftr_ct_path ] 
    [print(fl_phs[i]) for i in range(0,4)]
    fl_names=['h_t', 'h_c','f_t','f_c']
    for i in range(0,4):
        locals()[fl_names[i]]=data_reading(fl_phs[i],did_var)[2]  
        if i in (0,1):
            locals()[fl_names[i]]['Date'][0]='12/31/1978'
        else:
            locals()[fl_names[i]]['Date'][0]='12/31/2005'
        locals()[fl_names[i]]['Date']=pd.to_datetime(locals()[fl_names[i]]['Date'], format=format)
        locals()[fl_names[i]]=locals()[fl_names[i]].set_index(pd.DatetimeIndex(locals()[fl_names[i]]['Date']))
    return(locals()[fl_names[0]],locals()[fl_names[1]],locals()[fl_names[2]],locals()[fl_names[3]], did_var)
# h_t, h_c, f_t, f_c, did_var=did_prep(2,1,1, 2,'Foragers',36,2)
# =============================================================================
# DiD calculation modules
# =============================================================================
# Did on lowest values
def m1_lowest(h_t, h_c, f_t, f_c, did_var):
    h_t_min=h_t[did_var].min()
    h_c_min=h_c[did_var].min()
    f_t_min=f_t[did_var].min()
    f_c_min=f_c[did_var].min()
    cell_1_3=(f_t_min-h_t_min)
    cell_2_3=(f_c_min-h_c_min)
    cell_3_3= cell_1_3-cell_2_3
    title='Lowest values'
    did_results={'cell_1_1':h_t_min,'cell_2_1':h_c_min,'cell_1_2':f_t_min,'cell_2_2':f_c_min,'cell_1_3':cell_1_3,'cell_2_3':cell_2_3,'cell_3_3':cell_3_3, 'title': title}
    return(did_results)
# Did on mean values
def m2_mean(h_t, h_c, f_t, f_c, did_var):
    h_t_m2=h_t[did_var].mean()
    h_c_m2=h_c[did_var].mean()
    f_t_m2=f_t[did_var].mean()
    f_c_m2=f_c[did_var].mean()
    cell_1_3=(f_t_m2-h_t_m2)
    cell_2_3=(f_c_m2-h_c_m2)
    cell_3_3= cell_1_3-cell_2_3
    title='Mean values'
    did_results={'cell_1_1':h_t_m2,'cell_2_1':h_c_m2,'cell_1_2':f_t_m2,'cell_2_2':f_c_m2,'cell_1_3':cell_1_3,'cell_2_3':cell_2_3,'cell_3_3':cell_3_3,'title': title}
    return(did_results)
# =============================================================================
# Full DiD process 
# =============================================================================
def did(treatment_cnty, control_cnty, rcp, ftr_mdl,csd_f,csd_h, did_var, mode=[], hist_stt=[], hist_end=[], ftr_stt=[], ftr_end=[]): # treatment/control: source data; did_var: interested variable for DiD procedure;
    h_t, h_c, f_t, f_c, did_var=did_prep(treatment_cnty, control_cnty, rcp, ftr_mdl, did_var,csd_h=36, csd_f=csd_f)
    if  not mode or mode==0:
        did_results=m2_mean(h_t, h_c, f_t, f_c, did_var)
    else:
        did_results=m1_lowest(h_t, h_c, f_t, f_c, did_var)
    return(did_results)
# =============================================================================
# A full loop
# =============================================================================
ftr_append=[]
csd_append=[]
rcp_append=[]
cell_1_3_append=[]
cell_2_3_append=[]
cell_3_3_append=[]
for x in range(0,len(future_model_list)):
    ftr_mdl_na=future_model_list[x]
    for y in range(0,len(rcp_list)):
        rcp_na=rcp_list[y]
        for z in range(0, (len(cold_storage_period_list))):
            csd_na=cold_storage_period_list[z]
            did_re_temp=did(2, 1, y, x, z,36,"Foragers")
            ftr_append.append(future_model_list[x])
            csd_append.append(cold_storage_period_list[z])
            rcp_append.append(rcp_list[y])
            cell_1_3_append.append(did_re_temp['cell_1_3'])
            cell_2_3_append.append(did_re_temp['cell_2_3'])
            cell_3_3_append.append(did_re_temp['cell_3_3'])
            print(future_model_list[x],rcp_list[y],cold_storage_period_list[z])
d={'future model':ftr_append, 'cold storage periods':csd_append, 'rcp': rcp_append, 'treatment: after - before': cell_1_3_append, 'control: after - before': cell_2_3_append, 'DiD result': cell_3_3_append}
df=pd.DataFrame(d)
df.to_excel('DiD.xlsx')
ending_clock = datetime.now()
print(ending_clock-starting_clock)
# R7-3700x, 32GB, 0:54:07.689136
# Kamiak, 1 node, 56GB, 0:22:17.262247

# =============================================================================
# Appendix
# =============================================================================
# A1. Difference in difference (DID) procedures
# =============================================================================
#
# 2 X 2 difference in difference
# 
#             before | after       |  after-before
# treatment          |             |
# -------------------|-------------|------------
# control            |             |
# -------------------|-------------|------------
# difference - difference          |
# =============================================================================
# A2. Dictionaries
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
# rcp:
# rcp45: 0
# rcp85: 1
# =============================================================================
# A3. an alternative to write lists to files
# ftr_output= open('ftr_output.txt', 'w')
# simplejson.dump( ftr_append, ftr_output)
# ftr_output.close()
# 
# csd_output= open('csd_output.txt', 'w')
# simplejson.dump( ftr_append, csd_output)
# csd_output.close()
# 
# rcp_output= open('rcp_output.txt', 'w')
# simplejson.dump( rcp_append, rcp_output)
# rcp_output.close()
# 
# cell_1_3_output= open('cell_1_3_output.txt', 'w')
# simplejson.dump( cell_1_3_append, cell_1_3_output)
# cell_1_3_output.close()
# 
# cell_2_3_output= open('cell_2_3_output.txt', 'w')
# simplejson.dump( cell_2_3_append, cell_2_3_output)
# cell_2_3_output.close()
# 
# cell_3_3_output= open('cell_3_3_output.txt', 'w')
# simplejson.dump( cell_3_3_append, cell_3_3_output)
# cell_3_3_output.close()
# 
# =============================================================================








