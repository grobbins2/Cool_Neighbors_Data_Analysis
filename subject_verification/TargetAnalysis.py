#Code by Grady Robbins

#'http://byw.tools/wiseview#ra=242.9068549&dec=61.69279303&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd='

import numpy as np
import pandas as pd
import math
import re
import webbrowser

text_file = open(r"Cool_Neighbors_Subject_Verification\coolneighbors_sample-20230103.csv", "r")
usedID = []
counter = -1
first1 = True
first4 = True
first8 = True
first16 = True
first32 = True
id_samp = open(r"Cool_Neighbors_Subject_Verification/Sampleverify500.csv", "r")
for lineid in id_samp:
    templine = re.split(',',lineid)
    usedID.append(templine[0])

for line in text_file:
    counter +=1
    pattern1 = ',1,'
    pattern4 = ',4,'
    if re.search(pattern1, line) and first1 == True:
        starttype1 = counter
        first1 = False
    if re.search(pattern4,line) and first4 == True:
        endtype1 = counter
        first4 = False
endtype32 = counter
text_file.close()
type1rand = []
type4rand =  []
type8rand =  []
type16rand =  []
type32rand = []
counter = 0
print(starttype1,endtype1)
for l in range(1000):
    t1 = str(np.random.randint(starttype1,endtype1+1))
    while t1 in type1rand or t1 in usedID:
        t1 = str(np.random.randint(starttype1,endtype1+1))
    type1rand.append(t1)
type1links = []
type1RA = []
type1DEC = []
type1ID = []
text_file = open(r"Cool_Neighbors_Subject_Verification\coolneighbors_sample-20230103.csv", "r")
for linesamp in text_file:
    splitline = re.split(',',linesamp)
    pattern1 = ',1,'
    for l in range(len(type1rand)):
        if splitline[0] == type1rand[l]:
            type1ID.append(splitline[0])
            type1RA.append(splitline[1])
            type1DEC.append(splitline[2])
            type1links.append('http://byw.tools/wiseview#ra='+str(splitline[1])+'&dec='+str(splitline[2])+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
import csv
#type1rand = np.array(type1rand)
#type1links = np.array(type1links)
#with open(r'Cool_Neighbors_Subject_Verification\target1links.csv', 'w', newline='') as file:
#    for l in range(len(type1links)):
#        writer = csv.writer(file)
#        writer.writerow([type1ID[l],type1RA[l],type1DEC[l],type1links[l]])

value_list = []
validlink = []
validRA = []
validDEC = []
validID = []
linklist = []
RAlist = []
DEClist = []
IDlist = []
k=0
windowcount = 25
breaker = False
#print(type1rand)
with open(r'Cool_Neighbors_Subject_Verification\target1links.csv', 'r', newline='') as file:
    for line in file:
        if breaker == True:
                print(k)
                break
        templist = re.split(',',line)
        tempRA = templist[1]
        tempDEC = templist[2]
        tempID = templist[0]
        templink = templist[3]
        RAlist.append(tempRA)
        DEClist.append(tempDEC)
        IDlist.append(tempID)
        linklist.append(templink)
        if k/windowcount in (np.linspace(1,100,100)):
            for n in range(windowcount):
                webbrowser.open(linklist[n])
            value = (input('Is there a mover near the center of this frame? Y / N .'))
            val_temp = [*value]
            for l in range(len(val_temp)):
                if val_temp[l] == 'e':
                    breaker = True
                    break
                if val_temp[l] != 'N':
                    validlink.append(linklist[l])
                    validRA.append(RAlist[l])
                    validDEC.append(DEClist[l])
                    validID.append(IDlist[l])
            linklist = []
            linklist = []
            RAlist = []
            DEClist = []
            IDlist = []
            if breaker == True:
                print(k)
                break
        k+=1
print(k)

with open(r'Cool_Neighbors_Subject_Verification\target1.csv', 'w',newline='') as file:
    for l in range(len(validlink)):
        writer = csv.writer(file)
        writer.writerow([validID[l],validDEC[l],validRA[l],validlink[l]])
