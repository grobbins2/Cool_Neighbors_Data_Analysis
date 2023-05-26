# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:35:23 2022

@author: Noah Schapera, additionally edited by Grady Robbins
"""

import csv
import json 
import copy

target_RA = [16.7108298,210.3262329,190.4097772,359.1862397,235.4647919,357.8768151,144.7205969,165.0878656,358.9502545,66.01865451,80.94276174,302.9436792,208.4011539,341.9475301,312.5833209,233.6225199,323.2042298,235.4647919,344.1209961,213.0286759,161.9863979,16.36610597,60.64829526,136.4005774,50.29021863,342.7897743,224.6581785,234.7475954,314.7875697,8.782484709]

target_DEC = [22.86628829,43.43163896,-82.0143621,-48.24904634,52.50679211,-18.96675889,6.577807434,9.781231668,38.07750002,66.83637578,-54.88766233,-48.21651414,-0.632313207,-0.684836909,-25.61466829,-10.72049746,69.02053437,52.50679211,40.04105177,23.73669162,54.96145539,-78.57218915,-26.86263446,74.00313635,69.53459904,-7.677063248,17.58035594,48.44973152,2.684994576,-15.54261099]

class Parser:
    def __init__(self, subject_file_string_in,class_file_string_in):
        
        self.class_file_string = class_file_string_in
        self.subject_file_string = subject_file_string_in
        
        self.targets_classificationsToList()
        
        
        
    def stringToJson(self,string):
        '''
        Converts a string (metadata) to a json

        Parameters
        ----------
        string : String
            Any dictionary formatted as a string.

        Returns
        -------
        res : json object (dictionary)
            A dictionary.

        '''
        res = json.loads(string)
        return res
    
    def getUsersForSubject(self,subID):
        '''
        Returns users who contributed to a subject classification

        Parameters
        ----------
        subID : string
            ID of a particular subject of interest.

        Returns
        -------
        users : list, strings
            list of users who contributed to a subject classification.

        '''
        users = []
        for cl in self.classifications_list:
            classID = cl["subject_ids"]
            
            if subID == classID:
                users.append(cl["user_name"])
        return users    
    
    def getUniqueUsers(self):
        '''
        returns all unique users who contributed to a project

        Returns
        -------
        uniqueUsers : list, string
            list of all users who contributed to the project.

        '''
        uniqueUsers = []
        for cl in self.classifications_list:
            if len(uniqueUsers) == 0:
                uniqueUsers.append(cl["user_name"])
            else:
                isUnique = True
                for u in uniqueUsers:
                    if cl["user_name"] == u:
                        isUnique = False
                if isUnique:
                    uniqueUsers.append(cl["user_name"])
        return uniqueUsers
    
    def classifySubjectByThreshold(self,threshold,subID):
        '''
        iterates through classification list to find matches to a particular subect. Counts how many times each matching classification marks the subject as a mover. If its above a threshold, returns true

        Parameters
        ----------
        threshold : integer
            classification threshold.
        subID : string
            ID of a particular subject that is being matched.

        Returns
        -------
        bool
            true or false, has the number of classifications passed the threshold.
        yesCounter: int
            number of times the classifications were "Yes".

        '''
        yesCounter=0
        for cl in self.classifications_list:
            classID=cl["subject_ids"]

            
            if classID == subID:
                anno = self.stringToJson(cl["annotations"])
                if anno[0]["value"] == "Yes":
                    yesCounter+=1
        if yesCounter >= threshold:
            return True, yesCounter
        else:
            return False, 0

    def classifyAllSubjects(self,threshold):
        '''
        Iterates through all subjects and classifications, determines how many times each subject was classified as a mover. If the number of classifications is above
        a set threshold, returns the subject as a likely mover

        Parameters
        ----------
        threshold : Integer
            Number of times a subject must be classified as "yes" for it to be counted as a mover

        Returns
        -------
        movers : Nx2 list
            index [i][0] is the subject ID of the mover
            idex [i][1] is the number of times the mover was classified as "Yes"

        '''
        movers=[]

        for sub in self.subjects_list:
            subID=sub["subject_id"]
            isMover, numYes = self.classifySubjectByThreshold(threshold,subID)
            if isMover:
                mov=[subID,numYes]
                movers.append(mov)
        return movers
        
    
    def targets_classificationsToList(self):
    
        sub_file = open(self.subject_file_string, mode='r')
    
        class_file = open(self.class_file_string, mode='r')
        
        self.subjects_list = copy.deepcopy(list(csv.DictReader(sub_file)))
        self.classifications_list = copy.deepcopy(list(csv.DictReader(class_file)))
        
        class_file.close()
        sub_file.close()
        
class testParser(Parser):
    '''
    Child class of parser, for Cool Neighbors test
    '''
    def __init__(self, subject_file_string_in,class_file_string_in):
        super().__init__(subject_file_string_in,class_file_string_in)
        
    def printAccuracy(self):
        '''
        Compares known classifications (R/F) within the subjects hidden metadata to users classifications to determine accuracy.
        
        Only useful for this particular test
        Returns
        -------
        None.

        '''
        for sub in self.subjects_list:
            subBool = None
            metadata_json = self.stringToJson(sub["metadata"])
            subClass_RA = metadata_json["RA"]
            subClass_DEC = metadata_json["DEC"]
            for n in range(len(target_RA)):
                y=0
                if float(subClass_RA) <= (target_RA[n])*1.01 and float(subClass_RA) >= (target_RA[n])*0.98:
                    if float(subClass_DEC) <= target_DEC[n]*1.01 and float(subClass_DEC) >= target_DEC[n]*0.98:
                        subID = sub["subject_id"]
                    else:
                        y=1
                else:
                    y=1
        
                #else:
                #    subBool = False
                
                
            correctClass=0
            incorrectClass=0
            

            for cl in self.classifications_list:
                if y == 1:
                    break
                else:
                    
                    classID = cl["subject_ids"]
                    if classID == subID:
                        
                        anno = self.stringToJson(cl["annotations"])
                            
                        if anno[0]["value"] == "Yes":
                            clBool = True
                        else:
                            clBool = False
                                
                        if clBool == True:
                            correctClass += 1
                        else:
                            incorrectClass += 1
                            
                print(f"__pycache__s classified correctly {correctClass} times and incorrect {incorrectClass} times")
#--------------addition-------------        
import DataParser
import matplotlib.pyplot as plt
import numpy as np
P = DataParser.testParser('backyard-worlds-cool-neighbors-subjects.csv',
                          'backyard-worlds-cool-neighbors-classifications.csv')

ms = P.classifyAllSubjects(threshold=2)
us = P.getUniqueUsers()
acc = P.printAccuracy()

mover_name = []
mover_amount = []
count = np.zeros(30)
for m in ms:
    #print(m[0] + " was classified as a mover " + str(m[1]) + " times")
    mover_name.append(m[0])
    mover_amount.append(m[1])
    for n in range(0,30):
        if m[1] == n:
            count[n] += 1
#print(acc)
#print(count)
#for u in us:
#    print(u)
#plt.bar(np.linspace(0,30,30),count)
#plt.title('initial plot of mover vs reported movement')
#plt.ylabel('number of times object was classified as a mover')
#plt.xlabel('number of objects classified as mover')
#plt.show()
#plt.savefig('initialmoverplot_bar.png',dpi=300)



