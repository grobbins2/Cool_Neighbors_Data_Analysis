#Code by Grady Robbins

#'http://byw.tools/wiseview#ra=242.9068549&dec=61.69279303&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd='

import numpy as np
import pandas as pd
import math
import re
import webbrowser

text_file = open(r"Cool_Neighbors_Subject_Verification\coolneighbors_sample-20230103.csv", "r")

counter = -1
first1 = True
first4 = True
first8 = True
first16 = True
first32 = True
for line in text_file:
    counter +=1
    pattern1 = ',1,'
    pattern4 = ',4,'
    pattern8 = ',8,'
    pattern16 = ',16,'
    pattern32 = ',32,'
    if re.search(pattern1, line) and first1 == True:
        starttype1 = counter
        first1 = False
    if re.search(pattern4,line) and first4 == True:
        starttype4 = counter
        endtype1 = counter
        first4 = False
    if re.search(pattern8,line) and first8 == True:
        starttype8 = counter
        endtype4 = counter
        first8 = False
    if re.search(pattern16,line) and first16 == True:
        starttype16 = counter
        endtype8 = counter
        first16 = False
    if re.search(pattern32,line) and first32 == True:
        starttype32 = counter
        endtype16 = counter
        first32 = False
endtype32 = counter
text_file.close()
type1rand = []
type4rand =  []
type8rand =  []
type16rand =  []
type32rand = []
counter = 0
for l in range(100):
    t1 = str(np.random.randint(starttype1,endtype1+1))
    while t1 in type1rand:
        t1 = str(np.random.randint(starttype1,endtype1+1))
    t4 = str(np.random.randint(starttype4,endtype4+1))
    while t4 in type4rand:
        t4 = str(np.random.randint(starttype4,endtype4+1))
    t8 = str(np.random.randint(starttype8,endtype8+1))
    while t8 in type8rand:
        t8 = str(np.random.randint(starttype8,endtype8+1))
    t16 = str(np.random.randint(starttype16,endtype16+1))
    while t16 in type16rand:
        t16 = str(np.random.randint(starttype16,endtype16+1))
    t32 = str(np.random.randint(starttype32,endtype32+1))
    while t32 in type32rand:
        t32 = str(np.random.randint(starttype32,endtype32+1))
    type1rand.append(t1)
    type4rand.append(t4)
    type8rand.append(t8)
    type16rand.append(t16)
    type32rand.append(t32)
type1links = []
type4links = []
type8links = []
type16links = []
type32links = []
text_file = open(r"Cool_Neighbors_Subject_Verification\coolneighbors_sample-20230103.csv", "r")
for line in text_file:
    splitline = re.split(',',line)
    pattern1 = ',1,'
    pattern4 = ',4,'
    pattern8 = ',8,'
    pattern16 = ',16,'
    pattern32 = ',32,'
    if splitline[0] in type1rand:
        RA = splitline[1]
        DEC = splitline[2]
        type1links.append('http://byw.tools/wiseview#ra='+str(RA)+'&dec='+str(DEC)+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
    if splitline[0] in type4rand:
        RA = splitline[1]
        DEC = splitline[2]
        type4links.append('http://byw.tools/wiseview#ra='+str(RA)+'&dec='+str(DEC)+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
    if splitline[0] in type8rand:
        RA = splitline[1]
        DEC = splitline[2]
        type8links.append('http://byw.tools/wiseview#ra='+str(RA)+'&dec='+str(DEC)+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
    if splitline[0] in type16rand:
        RA = splitline[1]
        DEC = splitline[2]
        type16links.append('http://byw.tools/wiseview#ra='+str(RA)+'&dec='+str(DEC)+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
    if splitline[0] in type32rand:
        RA = splitline[1]
        DEC = splitline[2]
        type32links.append('http://byw.tools/wiseview#ra='+str(RA)+'&dec='+str(DEC)+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')

import csv
type1rand = np.array(type1rand)
type1links = np.array(type1links)
#print(len(set(type4rand)))

value_list = []
#text_file = open(r"Cool_Neighbors_Subject_Verification\Sampleverify500.csv", "r")
#for line in text_file:
    #link = re.split(',',line)[1]
    #webbrowser.open(link)
    #value = input('Is there a mover near the center of this frame? Y / N .')
    #with open('Cool_Neighbors_Subject_Verification\Sampletruth500.csv', 'w', newline='') as file:
    #    writer = csv.writer(file)
    #    writer.writerow([line,value])

#k=0
#with open(r'Cool_Neighbors_Subject_Verification\Sampleverify500 copy.csv', 'r', newline='') as file:
#    for line in file:
#        k+=1
#        if re.search('http',line):
#            link = re.split(',',line)[1]
#            webbrowser.open(link)
#            value = (input('Is there a mover near the center of this frame? Y / N .'))
#            if value == 'end':
#                break
#            value_list.append(value)
#print(counter)

#with open('Cool_Neighbors_Subject_Verification\Sampletruth500 copy.csv', 'w', newline='') as file:
#    for l in range(len(value_list)):
#        writer = csv.writer(file)
#        writer.writerow(value_list[l])
movelist = [0]
nomovelist = [0]
for l in [1,2,3,4,5]:
    movement = 0
    nomovement = 0
    k = -1
    with open(r'Cool_Neighbors_Subject_Verification\Sampletruth500.csv', 'r', newline='') as file:
        for line in file:
            if k == (l)*100 -1:
                break
            else:
                k+=1
                #print(k)
                if re.search('Y',line):
                    movement +=1
                if re.search('N',line):
                    nomovement +=1
    #print(k)
    movelist.append(movement)
    nomovelist.append(nomovement)
    movement = movement - movelist[l-1]
    nomovement = nomovement - nomovelist[l-1]
    if l == 1:
            print(movement,'movements, and',nomovement,'non-movements for type 1')
    else:
        print(movement,'movements, and',nomovement,'non-movements for type',2**(l))
