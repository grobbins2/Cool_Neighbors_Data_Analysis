"""
Created on Tuesday, May 16 2023

@author: Grady Robbins
"""

#analysis of targets true/false by type

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
typeRA = {'1':[],'2':[],'4':[],'8':[],'16':[]}
typeDEC = {'1':[],'2':[],'4':[],'8':[],'16':[]}

#separate RA and DEC by type
for line in beta_target_text:
    linesplit = re.split(',',line)
    #print(linesplit)
    for i in range(5):
        if str(2**i)+'\n' in linesplit[2]:
            typeRA[str(2**i)].append(str(linesplit[0]))
            typeDEC[str(2**i)].append(str(linesplit[1]))

type_presence = 0
typedata = {'1':[],'2':[],'4':[],'8':[],'16':[]}
patterntype = {'1':'"#Type"":""1"','2':'"#Type"":""2"','4':'"#Type"":""4"','8':'"#Type"":""8"','16':'"#Type"":""16"'}
#read in data and search for specific type
final_counter = 0
bad_ID = [78412786,78412838,78517043,78517056,79925646,79925663,78412820,78517052,79925658] # this ID should not be counted. as the targets are not verified
#separate data by type and remove bad IDs
for line in beta_class_text:
    if re.search(patterntype['1'], line):
        typedata['1'].append(line)
    if re.search(patterntype['2'], line):
        typedata['2'].append(line)
    if re.search(patterntype['4'], line):
        bad_ID_counter = 0
        for n in range(len(bad_ID)):
            if str(bad_ID[n]) in line:
                bad_ID_counter = 1
        if bad_ID_counter != 1:
            typedata['4'].append(line)
    if re.search(patterntype['8'], line):
        typedata['8'].append(line)
    if re.search(patterntype['16'], line):
        typedata['16'].append(line)

move_count = {'1':0,'2':0,'4':0,'8':0,'16':0}
nomove_count = {'1':0,'2':0,'4':0,'8':0,'16':0}
#determine movement counts by type
for i in range(5):
    for l in range(len(typedata[str(2**i)])):
        if "Yes" in typedata[str(2**i)][l]:
            move_count[str(2**i)] +=1
        if "No" in typedata[str(2**i)][l]:
            nomove_count[str(2**i)] +=1
    for l in range(len(typedata[str(2**i)])):
        for k in range(len(RA)):
            if str(int(RA[k])) in typedata[str(2**i)][l] and str(int(DEC[k])) in typedata[str(2**i)][l]:
                final_counter +=1
                break
        for k in range(len(typeRA[str(2**i)])):
            if typeRA[str(2**i)][k] in typedata[str(2**i)][l] and typeDEC[str(2**i)][k] in typedata[str(2**i)][l]:
                type_presence +=1
                break
    print('there were',move_count[str(2**i)],'movement decisions and',nomove_count[str(2**i)],'nonmovement decisions on type',str(2**i),'targets, giving a ratio of', (move_count[str(2**i)])/(move_count[str(2**i)]+nomove_count[str(2**i)])*100, '%')

print('there are ',move_count['1']+move_count['2']+move_count['4']+move_count['8']+move_count['16']+nomove_count['1']+nomove_count['2']+nomove_count['4']+nomove_count['8']+nomove_count['16'],'total targets used and',11026,'targets present')
