"""
This script generates ProtSIQ using PepsSIQ.

"""

#Import

import csv

#Constant

file1 = open("dsname.txt")
DatasetName = file1.read()
file1.close()
PepsSIQ_PATH = DatasetName+'PepSIQ.csv'

#Programmes

def Average(lst):
    return sum(lst) / len(lst)

def Range(number):
    if number is 0:
        return 0
    elif number < 1:
        return 0.5
    elif number < 2:
        return 1
    elif number < 3:
        return 2
    elif number < 5:
        return 3
    elif number < 10:
        return 5
    elif number < 50:
        return 10
    elif number < 100:
        return 50 #50 means in range 50-100
    elif number < 500:
        return 100
    else:
        return 500

#Import data

with open(PepsSIQ_PATH, mode ='r') as datafile:
    PepSIQ_data = datafile.read()

#Create ProtSIQ - Sum Everything From PepsSIQ

ProtSIQ_Dict=dict() #Everything is summed into this dictionary
PepSIQ_rows = PepSIQ_data.splitlines()
for row in PepSIQ_rows[1:]:
    split = row.split(',')
    group = split[1]
    pepseq = split[2]
    NumLoci = split[3]
    AGI = split[5]
    SampleGroup_AGI = group+'|'+AGI
    if SampleGroup_AGI not in ProtSIQ_Dict.keys(): 
        ProtSIQ_Dict[SampleGroup_AGI] = dict() #Make empty dictionary to be filled if this SampleGroup is new
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluPeps_R1'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluPeps_R2'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluPeps_R3'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbPeps_R1'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbPeps_R2'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbPeps_R3'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluSpecs_R1'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluSpecs_R2'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluSpecs_R3'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbSpecs_R1'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbSpecs_R2'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbSpecs_R3'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIExcluPeps_R1'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIExcluPeps_R2'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIExcluPeps_R3'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIAmbPeps_R1'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIAmbPeps_R2'] = 0
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIAmbPeps_R3'] = 0   
    if NumLoci is '1': #Exclusive Peptides
        if split[8] is not '0': #If NumSpecs is >0, add that a peptide is counted
            ProtSIQ_Dict[SampleGroup_AGI]['#ExcluPeps_R1'] += 1
        if split[9] is not '0':
            ProtSIQ_Dict[SampleGroup_AGI]['#ExcluPeps_R2'] += 1
        if split[10] is not '0':
            ProtSIQ_Dict[SampleGroup_AGI]['#ExcluPeps_R3'] += 1
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluSpecs_R1'] += float(split[8]) 
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluSpecs_R2'] += float(split[9])
        ProtSIQ_Dict[SampleGroup_AGI]['#ExcluSpecs_R3'] += float(split[10])
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIExcluPeps_R1'] += float(split[11]) 
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIExcluPeps_R2'] += float(split[12])
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIExcluPeps_R3'] += float(split[13])
    else: #Ambiguous Peptides. No peptides have Numloci 0
        if split[8] is not '0':
            ProtSIQ_Dict[SampleGroup_AGI]['#AmbPeps_R1'] += 1
        if split[9] is not '0':
            ProtSIQ_Dict[SampleGroup_AGI]['#AmbPeps_R2'] += 1
        if split[10] is not '0':
            ProtSIQ_Dict[SampleGroup_AGI]['#AmbPeps_R3'] += 1
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbSpecs_R1'] += float(split[8]) 
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbSpecs_R2'] += float(split[9])
        ProtSIQ_Dict[SampleGroup_AGI]['#AmbSpecs_R3'] += float(split[10])
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIAmbPeps_R1'] += float(split[11]) 
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIAmbPeps_R2'] += float(split[12])
        ProtSIQ_Dict[SampleGroup_AGI]['ProtIAmbPeps_R3'] += float(split[13])

# Calculations
for key in ProtSIQ_Dict.keys():
    Peps_E = [ProtSIQ_Dict[key]['#ExcluPeps_R1'], ProtSIQ_Dict[key]['#ExcluPeps_R2'], ProtSIQ_Dict[key]['#ExcluPeps_R3']]
    ProtSIQ_Dict[key]['MeanPeps_E'] = Average(Peps_E)
    ProtSIQ_Dict[key]['MaxPeps_E'] = max(Peps_E)
    Peps_A = [ProtSIQ_Dict[key]['#AmbPeps_R1'], ProtSIQ_Dict[key]['#AmbPeps_R2'], ProtSIQ_Dict[key]['#AmbPeps_R3']]
    ProtSIQ_Dict[key]['MeanPeps_A'] = Average(Peps_A)
    ProtSIQ_Dict[key]['MaxPeps_A'] = max(Peps_A)
    Specs_E = [ProtSIQ_Dict[key]['#ExcluSpecs_R1'], ProtSIQ_Dict[key]['#ExcluSpecs_R2'], ProtSIQ_Dict[key]['#ExcluSpecs_R3']]
    ProtSIQ_Dict[key]['MeanSpecs_E'] = Average(Specs_E)
    ProtSIQ_Dict[key]['MaxSpecs_E'] = max(Specs_E)
    Specs_A = [ProtSIQ_Dict[key]['#AmbSpecs_R1'], ProtSIQ_Dict[key]['#AmbSpecs_R2'], ProtSIQ_Dict[key]['#AmbSpecs_R3']]
    ProtSIQ_Dict[key]['MeanSpecs_A'] = Average(Specs_A)
    ProtSIQ_Dict[key]['MaxSpecs_A'] = max(Specs_A)
    ProtSIQ_Dict[key]['Protein E/A'] = 'NA'
    ProtSIQ_Dict[key]['Protein E/A'] = 'A' #Set every peptide to A, then overwrite to E value if MeanPeps_E is not 0
    ProtSIQ_Dict[key]['MeanPeps_E/A'] = ProtSIQ_Dict[key]['MeanPeps_A']
    ProtSIQ_Dict[key]['MaxPeps_E/A'] = ProtSIQ_Dict[key]['MaxPeps_A']
    ProtSIQ_Dict[key]['MeanSpecs_E/A'] = ProtSIQ_Dict[key]['MeanSpecs_A']
    ProtSIQ_Dict[key]['MaxSpecs_E/A'] = ProtSIQ_Dict[key]['MaxSpecs_A']
    if ProtSIQ_Dict[key]['MeanPeps_E'] is not 0:
        ProtSIQ_Dict[key]['Protein E/A'] = 'E'
        ProtSIQ_Dict[key]['MeanPeps_E/A'] = ProtSIQ_Dict[key]['MeanPeps_E']
        ProtSIQ_Dict[key]['MaxPeps_E/A'] = ProtSIQ_Dict[key]['MaxPeps_E']
        ProtSIQ_Dict[key]['MeanSpecs_E/A'] = ProtSIQ_Dict[key]['MeanSpecs_E']
        ProtSIQ_Dict[key]['MaxSpecs_E/A'] = ProtSIQ_Dict[key]['MaxSpecs_E']
    ProtSIQ_Dict[key]['MeanPepsCat_E/A'] = Range(ProtSIQ_Dict[key]['MeanPeps_E/A'])
    ProtSIQ_Dict[key]['MaxPepsCat_E/A'] = Range(ProtSIQ_Dict[key]['MaxPeps_E/A'])
    ProtSIQ_Dict[key]['MeanSpecsCat_E/A'] = Range(ProtSIQ_Dict[key]['MeanSpecs_E/A'])
    ProtSIQ_Dict[key]['MaxSpecsCat_E/A'] = Range(ProtSIQ_Dict[key]['MaxSpecs_E/A'])

#Generate list of lists for csv file

Output_csv_list = list()
for key in ProtSIQ_Dict.keys():
    ordered_list = list()
    ordered_list.append(key) #SampleGroup|AGI
    ordered_list.append(key.split('|')[0]) #SampleGroup
    ordered_list.append(key.split('|')[1]) #AGI
    ordered_list.append(ProtSIQ_Dict[key]['ProtIExcluPeps_R1'])
    ordered_list.append(ProtSIQ_Dict[key]['ProtIExcluPeps_R2'])
    ordered_list.append(ProtSIQ_Dict[key]['ProtIExcluPeps_R3'])
    ordered_list.append(ProtSIQ_Dict[key]['ProtIAmbPeps_R1'])
    ordered_list.append(ProtSIQ_Dict[key]['ProtIAmbPeps_R2'])
    ordered_list.append(ProtSIQ_Dict[key]['ProtIAmbPeps_R3'])
    ordered_list.append(ProtSIQ_Dict[key]['#ExcluPeps_R1'])
    ordered_list.append(ProtSIQ_Dict[key]['#ExcluPeps_R2'])
    ordered_list.append(ProtSIQ_Dict[key]['#ExcluPeps_R3'])
    ordered_list.append(ProtSIQ_Dict[key]['#AmbPeps_R1'])
    ordered_list.append(ProtSIQ_Dict[key]['#AmbPeps_R2'])
    ordered_list.append(ProtSIQ_Dict[key]['#AmbPeps_R3'])
    ordered_list.append(ProtSIQ_Dict[key]['#ExcluSpecs_R1'])
    ordered_list.append(ProtSIQ_Dict[key]['#ExcluSpecs_R2'])
    ordered_list.append(ProtSIQ_Dict[key]['#ExcluSpecs_R3'])
    ordered_list.append(ProtSIQ_Dict[key]['#AmbSpecs_R1'])
    ordered_list.append(ProtSIQ_Dict[key]['#AmbSpecs_R2'])
    ordered_list.append(ProtSIQ_Dict[key]['#AmbSpecs_R3'])
    ordered_list.append(ProtSIQ_Dict[key]['Protein E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanPeps_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxPeps_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanSpecs_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxSpecs_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanPepsCat_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxPepsCat_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanSpecsCat_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxSpecsCat_E/A'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanPeps_E'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanPeps_A'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanSpecs_E'])
    ordered_list.append(ProtSIQ_Dict[key]['MeanSpecs_A'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxPeps_E'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxPeps_A'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxSpecs_E'])
    ordered_list.append(ProtSIQ_Dict[key]['MaxSpecs_A'])
    Output_csv_list.append(ordered_list)


#Save

Fields = ['SampleGroup|AGI', 'SampleGroup', 'AGI', 'ProtIExcluPeps_R1', 'ProtIExcluPeps_R2', 'ProtIExcluPeps_R3', 'ProtIAmbPeps_R1', 'ProtIAmbPeps_R2','ProtIAmbPeps_R3','#ExcluPeps_R1','#ExcluPeps_R2','#ExcluPeps_R3','#AmbPeps_R1','#AmbPeps_R2','#AmbPeps_R3','#ExcluSpecs_R1'
,'#ExcluSpecs_R2','#ExcluSpecs_R3','#AmbSpecs_R1','#AmbSpecs_R2','#AmbSpecs_R3','Protein E/A','MeanPeps_E/A','MaxPeps_E/A','MeanSpecs_E/A','MaxSpecs_E/A','MeanPepsCat_E/A','MaxPepsCat_E/A','MeanSpecsCat_E/A','MaxSpecsCat_E/A','MeanPeps_E','MeanPeps_A','MeanSpecs_E','MeanSpecs_A'
, 'MaxPeps_E','MaxPeps_A','MaxSpecs_E','MaxSpecs_A']
filename = DatasetName + 'ProtSIQ.csv'
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(Output_csv_list)

