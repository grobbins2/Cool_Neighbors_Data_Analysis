"""
Created on Wednesday, May 17 2023

@author: Grady Robbins
"""

import numpy as np
import pandas as pd
import math
import re
import csv

beta_classifications = r'Cool_Neighbors_Beta_Accuracy\beta_workflow-classifications (1) (1).csv'
beta_targets = r'Cool_Neighbors_Beta_Accuracy\beta_targets_final.csv'
coord_data = np.loadtxt(beta_targets,delimiter=',',usecols=(0,1)).astype(float)
beta_class_text = open(beta_classifications, "r")
beta_target_text = open(beta_targets, 'r')

RA = coord_data[:,0]
DEC = coord_data[:,1]
#define values for type of target, here 2^(0,1,2,3,4,5) used
typeRA = {'1':[],'2':[],'4':[],'8':[],'16':[]}
typeDEC = {'1':[],'2':[],'4':[],'8':[],'16':[]}

#separate RA and DEC by target type
text_filecoord = open(beta_targets,'r')
for line in text_filecoord:
    linesplit = re.split(',',line)
    for i in range(5):
        if str(2**i)+'\n' in linesplit[2]:
            typeRA[str(2**i)].append(str(linesplit[0]))
            typeDEC[str(2**i)].append(str(linesplit[1]))

type_presence = 0
typedata = {'1':[],'2':[],'4':[],'8':[],'16':[]}
patterntype = {'1':'"#Type"":""1"','2':'"#Type"":""2"','4':'"#Type"":""4"','8':'"#Type"":""8"','16':'"#Type"":""16"'}

#separate data by type and remove bad IDs
final_counter = 0
bad_ID = [78412786,78412838,78517043,78517056,79925646,79925663,78412820,78517052,79925658] # this ID should not be counted. as the targets are not verified
for line in beta_class_text:
    if re.search(patterntype['1'], line):
        typedata['1'].append(line)
    if re.search(patterntype['2'], line):
        typedata['2'].append(line)
    if re.search(patterntype['4'], line):
        p = 0
        for n in range(len(bad_ID)):
            if str(bad_ID[n]) in line:
                p = 1
        if p != 1:
            typedata['4'].append(line)
    if re.search(patterntype['8'], line):
        typedata['8'].append(line)
    if re.search(patterntype['16'], line):
        typedata['16'].append(line)

#read in data and search for specific types

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

#calculate RA,DEC,link, and accuracy per target by type and write on csv

RA_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
DEC_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
link_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
count_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
totalcount_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
acceptance_ratio = 0.3
for i in range(5):
    for n in range(len(typeRA[str(2**i)])):
        true_values = 0
        total_values = 0
        for k in range(len(typedata[str(2**i)])):
            if '""RA"":""'+str(round_down(float(typeRA[str(2**i)][n]),2)) in typedata[str(2**i)][k]:
                if '""DEC"":""'+str(int(float(typeDEC[str(2**i)][n])))+'.' in typedata[str(2**i)][k]:
                    total_values +=1
                    if 'Yes' in typedata[str(2**i)][k]:
                        true_values +=1
                        data_temp = typedata[str(2**i)][k]
        if total_values != 0:
            if true_values/total_values <= acceptance_ratio:
                totalcount_ratio[str(2**i)].append(total_values)
                count_ratio[str(2**i)].append(int(true_values))
                value_list = re.split(',',data_temp)
                for l in value_list:
                    if 'byw' in l:
                        RA_ratio[str(2**i)].append(typeRA[str(2**i)][n])
                        DEC_ratio[str(2**i)].append(typeDEC[str(2**i)][n])
                        link_ratio[str(2**i)].append('http://byw.tools/wiseview#ra='+typeRA[str(2**i)][n]+'&dec='+typeDEC[str(2**i)][n]+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')

#write on file
    with open(r'Cool_Neighbors_Beta_Accuracy\type'+str(str(2**i))+'ratios.csv','w', newline = '') as file:
        writer = csv.writer(file)
        for k in range(len(link_ratio[str(2**i)])):
            writer.writerow([count_ratio[str(2**i)][k]/totalcount_ratio[str(2**i)][k],RA_ratio[str(2**i)][k],DEC_ratio[str(2**i)][k],link_ratio[str(2**i)][k]])
