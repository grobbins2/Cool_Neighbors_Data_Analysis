"""
Created on Wednesday, May 17 2023

@author: Grady Robbins
"""


#Calculate accuracy of targets dependent on determined difficulty
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

text_filecoord = open(beta_targets,'r')
#separate RA and DEC by target type
for line in text_filecoord:
    linesplit = re.split(',',line)
    #print(linesplit)
    for i in range(5):
        if str(2**i)+'\n' in linesplit[2]:
            typeRA[str(2**i)].append(str(linesplit[0]))
            typeDEC[str(2**i)].append(str(linesplit[1]))


#find true and false values for ID's dependent on difficulty rating
difficultyID_group = {'easy':[],'medium':[],'difficult':[]}
text_file_dim = open(r"Cool_Neighbors_Beta_Accuracy\type4dimmness.csv", "r") #text file with difficulty information
for line_dim in text_file_dim:
    for i in ['easy','medium','difficult']:
        if i in line_dim:
            difficulty_data = re.split(',',line_dim)
            difficulty_data = difficulty_data[-1]
            difficultyID_group[i].append(difficulty_data)

difficultyID = {'easy':[],'medium':[],'difficult':[]}
for i in ['easy','medium','difficult']:
    for k in range(len(difficultyID_group[i])):
        length = re.split(' ',difficultyID_group[i][k])[:-1]
        for n in range(len(length)):
            difficultyID[i].append(length[n])

difficulty_true = {'easy' : 0,'medium' : 0,'difficult' : 0}
difficulty_false = {'easy' : 0,'medium' : 0,'difficult' : 0}
beta_class_text = open(beta_classifications, "r")
for line_BD in beta_class_text:
    for i in ['easy','medium','difficult']:
        for k in range(len(difficultyID[i])):
            if difficultyID[i][k] in line_BD:
                if 'Yes' in line_BD:
                    difficulty_true[i] +=1
                if 'No' in line_BD:
                    difficulty_false[i]+=1

for i in ['easy','medium','difficult']:
    print(difficulty_true[i],'true decisions for',i,'BDs and',difficulty_false[i],'false decisions for',i,'BDs, giving an easy accuracy of',difficulty_true[i]/(difficulty_true[i]+difficulty_false[i])*100,'%')
#test for repeated ID
for n in range(len(difficultyID['easy'])):
    for k in range(len(difficultyID['medium'])):
        for l in range(len(difficultyID['difficult'])):
            if difficultyID['easy'][n] == difficultyID['medium'][k] or difficultyID['easy'][n] == difficultyID['difficult'][l] or difficultyID['medium'][k] == difficultyID['difficult'][l]:
                print('error: repeated ID')