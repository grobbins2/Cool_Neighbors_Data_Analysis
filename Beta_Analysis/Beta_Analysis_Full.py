"""
Created on Wednesday, May 16 2023

@author: Grady Robbins
"""

#analysis of Cool Neighbors Beta Test Results in Full Code, recommended to use individual codes instead

import numpy as np
import pandas as pd
import math
import re
import csv

beta_classifications = r'C:\Users\Gradondosaurus Rex\Documents\Cool Neighbors Main\Cool Neighbors\Cool_Neighbors_Beta_Accuracy\beta_workflow-classifications (1) (1).csv'
beta_targets = r'C:\Users\Gradondosaurus Rex\Documents\Cool Neighbors Main\Cool Neighbors\Cool_Neighbors_Beta_Accuracy\beta_targets_final.csv'
coord_data = np.loadtxt(r'C:\Users\Gradondosaurus Rex\Documents\Cool Neighbors Main\Cool Neighbors\Cool_Neighbors_Beta_Accuracy\beta_targets_final.csv',delimiter=',',usecols=(0,1)).astype(float)
beta_class_text = open(beta_classifications, "r")
beta_target_text = open(beta_targets, 'r')
RA = coord_data[:,0]
DEC = coord_data[:,1]
typeRA = {'1':[],'2':[],'4':[],'8':[],'16':[]}
typeDEC = {'1':[],'2':[],'4':[],'8':[],'16':[]}
#"2^0 is dan ML targets, 2^1 is 2016 search targets, 2^2 is known BD, 2^3 is quasar, 2^4 is random sky"
text_filecoord = open(beta_targets,'r')
for line in text_filecoord:
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

move_count = {'1':0,'2':0,'4':0,'8':0,'16':0}
nomove_count = {'1':0,'2':0,'4':0,'8':0,'16':0}
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

#-------------------begin initial plots-----------
import matplotlib.pyplot as plt

types = ('known BD','Quasars','Random Sky')
weight_counts = {
    "No Movement": (nomove_count['4'],nomove_count['8'],nomove_count['16']),
    "Movement": (move_count['4'],move_count['8'],move_count['16']),
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(types, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Reported movement in targets")
ax.legend(loc="upper right")
plt.xlabel('target type')
plt.ylabel('number of targets')
#plt.savefig(r'Cool_Neighbors_Beta_Accuracy\Movement_bar_Betareduced.png',dpi=300)
plt.close()

types = ('known BD','Quasars','Random Sky')
weight_counts = {
    "Incorrect": (nomove_count['4'],move_count['8'],move_count['16']),
    "Correct": (move_count['4'],nomove_count['8'],nomove_count['16']),
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(types, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Accuracy of Beta Testers by Target Class")
ax.legend(loc="upper right")
plt.xlabel('target type')
plt.ylabel('number of classifications')
#plt.savefig(r'Cool_Neighbors_Beta_Accuracy\Accuracy_bar_Betareduced.png',dpi=300)
plt.close()
#-----------------background check on beta targets final RA,DEC,Type-------------
fin_reverse = []
for line in beta_target_text:
    fin_reverse.append(re.split(',',line))
reverse_counter = 0
for l in range(len(fin_reverse)):
    for k in range(len(RA)):
        if str(int(RA[k])) in fin_reverse[l] and str(int(DEC[k])) in fin_reverse[l]:
            reverse_counter +=1
            break
print(final_counter/11026*100,'% of the objects in the beta workflow classifications csv are present in the beta targets final csv (',final_counter,')')
print(reverse_counter/275*100,'% of the objects in the beta targets final csv are present in the beta workflow classifications csv (',(reverse_counter),')')
print(type_presence/11026*100,'% of the beta targets\' type match with the type of the final target classifications csv (',type_presence,')' )
#reduced amounts acceptable due to bad ID data

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

#----------------check all target yes/total ratios-----------
RA_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
DEC_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
link_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
count_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
totalcount_ratio = {'1':[],'2':[],'4':[],'8':[],'16':[]}
acceptance = 0.3
for i in range(5):
    for n in range(len(typeRA[str(2**i)])):
        val_true = 0
        total_val = 0
        for k in range(len(typedata[str(2**i)])):
            if '""RA"":""'+str(round_down(float(typeRA[str(2**i)][n]),2)) in typedata[str(2**i)][k]:
                if '""DEC"":""'+str(int(float(typeDEC[str(2**i)][n])))+'.' in typedata[str(2**i)][k]:
                    total_val +=1
                    if 'Yes' in typedata[str(2**i)][k]:
                        val_true +=1
                        data_temp = typedata[str(2**i)][k]
        if total_val != 0:
            if val_true/total_val <= acceptance:
                totalcount_ratio[str(2**i)].append(total_val)
                count_ratio[str(2**i)].append(int(val_true))
                val_list = re.split(',',data_temp)
                for l in val_list:
                    if 'byw' in l:
                        RA_ratio[str(2**i)].append(typeRA[str(2**i)][n])
                        DEC_ratio[str(2**i)].append(typeDEC[str(2**i)][n])
                        link_ratio[str(2**i)].append('http://byw.tools/wiseview#ra='+typeRA[str(2**i)][n]+'&dec='+typeDEC[str(2**i)][n]+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=0&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
#write on file
    with open(r'Cool_Neighbors_Beta_Accuracy\type'+str(str(2**i))+'ratios.csv','w', newline = '') as file:
        writer = csv.writer(file)
        for k in range(len(link_ratio[str(2**i)])):
            writer.writerow([count_ratio[str(2**i)][k]/totalcount_ratio[str(2**i)][k],RA_ratio[str(2**i)][k],DEC_ratio[str(2**i)][k],link_ratio[str(2**i)][k]])

#--------------------find dimness in known BD's and compare them to beta result accuracy
type4subjects =[]
type4ID = []
subject_txt = open(r'Cool_Neighbors_Beta_Accuracy\backyard-worlds-cool-neighbors-subjects (1).csv','r')

dimness_list = []
for sub_line in subject_txt:
    for k in range(len(typeRA['4'])):
        if re.search('""RA"":""'+str(round_down(float(typeRA['4'][k]),2))+'.',sub_line):
            if re.search('""DEC"":""'+((typeDEC['4'][k]))+'.',sub_line):
                type4subjects.append(sub_line)
                idtemp = re.split(',',sub_line)
                for n in range(len(idtemp)):
                    if '"ID"' in idtemp[n]:
                        type4ID.append(idtemp[n])
                        dimness_list.append(str(typeRA['4'][k])+':'+str(typeDEC['4'][k])+':'+str(idtemp[n]))

#find true and false values dependent on difficulty rating
diffID = {'easy':[],'medium':[],'difficult':[]}
text_file_dim = open(r"Cool_Neighbors_Beta_Accuracy\type4dimmness.csv", "r")
for line_dim in text_file_dim:
    for i in ['easy','medium','difficult']:
        if i in line_dim:
            diff_data = re.split(',',line_dim)
            diff_data = diff_data[-1]
            diffID[i].append(diff_data)

dif = {'easy':[],'medium':[],'difficult':[]}
for i in ['easy','medium','difficult']:
    for k in range(len(diffID[i])):
        length = re.split(' ',diffID[i][k])[:-1]
        for n in range(len(length)):
            dif[i].append(length[n])

type4ID = list(set(type4ID))
difficulty_true = {'easy' : 0,'medium' : 0,'difficult' : 0}
difficulty_false = {'easy' : 0,'medium' : 0,'difficult' : 0}
beta_class_text = open(beta_classifications, "r")
for line_BD in beta_class_text:
    for i in ['easy','medium','difficult']:
        for k in range(len(dif[i])):
            if dif[i][k] in line_BD:
                if 'Yes' in line_BD:
                    difficulty_true[i] +=1
                if 'No' in line_BD:
                    difficulty_false[i]+=1

for i in ['easy','medium','difficult']:
    print(difficulty_true[i],'true decisions for',i,'BDs and',difficulty_false[i],'false decisions for',i,'BDs, giving an easy accuracy of',difficulty_true[i]/(difficulty_true[i]+difficulty_false[i])*100,'%')

for n in range(len(dif['easy'])):
    for k in range(len(dif['medium'])):
        for l in range(len(dif['difficult'])):
            if dif['easy'][n] == dif['medium'][k] or dif['easy'][n] == dif['difficult'][l] or dif['medium'][k] == dif['difficult'][l]:
                print('error: repeated ID')
#---------------------------individual subject analysis-------------------------
individual_true = np.zeros([29])
individual_false = np.zeros([29])

for line_BD in beta_class_text:
    n=-1
    line_BD = line_BD
    for line_dim in text_file_dim:
        n+=1
        diff_data = re.split(',',line_dim)
        diff_data = diff_data[-1]
        dim_data = re.split(' ',diff_data)[:-1]
        for l in range(len(dim_data)):
            if str(dim_data[l]) in line_BD:
                if 'Yes' in line_BD:
                    individual_true[n] +=1
                    break
                if 'No' in line_BD:
                    individual_false[n] +=1
                    break
print('the total true and false responses add to',np.sum(individual_false),np.sum(individual_true))
print('true values:',individual_true.astype(int))
print('false values:',individual_false.astype(int))
print(individual_true/(individual_true+individual_false)*100,'%')

#plotting

difficulty = ('easy','medium','difficult')
weight_counts = {
    "Incorrect": (difficulty_false['easy'],difficulty_false['medium'],difficulty_false['difficult']),
    "Correct": (difficulty_true['easy'],difficulty_true['medium'],difficulty_true['difficult']),
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    pp = ax.bar(difficulty, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count
ax.set_title("Accuracy Depending on Difficulty")
ax.legend(loc="upper right")
plt.xlabel('Difficulty Rating')
plt.ylabel('number of classifications')


#plt.savefig(r'Cool_Neighbors_Beta_Accuracy\Difficulty_Accuracy_Beta.png',dpi=300)

plt.close()
print('total accuracy of 89.12%')

#---------------------compare accuracy to retirement limit, find false positive and negative rate------------
from scipy.stats import binom
import matplotlib.pyplot as plt
def estimate_false_positive_rate(retirement_limit, threshold_votes):
    # Define the parameters
    total_votes = retirement_limit
    yes_votes_needed = threshold_votes

    # Calculate the probability of obtaining at least the threshold number of "yes" votes
    probability = 1-binom.cdf(yes_votes_needed - 1, total_votes, 0.63)

    # Estimate the false positive rate
    false_positive_rate = probability * 100

    return false_positive_rate
limit_list = list(np.linspace(18,24,7))
prob_list_majority = np.zeros(7)
prob_list_third = np.zeros(7)
for l in range(len(limit_list)):
    vote_list_majority = (limit_list[l]*0.5)
    threshold_votes = vote_list_majority #number of votes until we conclude an object is indeed a mover
    retirement_limit = limit_list[l]
    false_positive_rate = estimate_false_positive_rate(retirement_limit, threshold_votes)
    prob_list_majority[l] = false_positive_rate

# Example usage
#retirement_limit = 20
#threshold_votes =6
#false_positive_rate = estimate_false_positive_rate(retirement_limit, threshold_votes)
#print(prob_list_majority)
print(f"False positive rate: { false_positive_rate:.4f}%")
plt.bar(limit_list,prob_list_majority)
plt.title('Retirement limit vs accuracy if majority required to consider mover')
plt.xlabel('Retirement Limit')
plt.ylabel('chance of false positive (%)')
#plt.savefig(r'Cool_Neighbors_Beta_Accuracy\retire_vs_accuracy_maj.png',dpi=300)
#plt.show()
plt.close()
for l in range(len(limit_list)):
    vote_list_majority = (limit_list[l]*0.3)
    #if vote_list_majority.is_integer() == True:
    #    vote_list_majority -=1
    #if vote_list_majority.is_integer() == False:
    #    vote_list_majority = int(vote_list_majority)
    threshold_votes = vote_list_majority #number of votes until we conclude an object is indeed a mover
    retirement_limit = limit_list[l]
    false_positive_rate = estimate_false_positive_rate(retirement_limit, threshold_votes)
    prob_list_third[l] = false_positive_rate
plt.bar(limit_list,prob_list_third)
plt.title('Retirement limit vs accuracy if 30% required to consider mover')
plt.xlabel('Retirement Limit')
plt.ylabel('chance of false positive (%)')
#plt.savefig(r'Cool_Neighbors_Beta_Accuracy\retire_vs_accuracy_third.png',dpi=300)
#plt.show()
plt.close()
