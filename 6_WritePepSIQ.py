"""
This script generates PepSIQ using Data3 and PepsExp
first, Data3 is inspected and the NumPSMs and NormInt for each peptide is noted for each replicate in dictionaries.

"""

#Import

import csv

#Constant

file1 = open("dsname.txt")
DatasetName = file1.read()
file1.close()
Data3PATH = DatasetName+'Data3.csv'
Peps_ExpPATH = DatasetName+'Peps_Exp.csv'

#Import data

with open(Data3PATH, mode ='r') as datafile:
    Data3_data = datafile.read()
with open(Peps_ExpPATH, mode ='r') as datafile:
    PepsExp_data = datafile.read()

#Extract #Specs R1-3 and PepInt R1-3

NormIntDICT = dict()
NumPSMsDICT = dict()
Groups = list()
Data3_rows = Data3_data.splitlines()
for row in Data3_rows[1:]:
    split = row.split(',')
    Name = split[0]
    NormInt = split[6]
    NumPSMs = split[7]
    group = split[2]
    pepseq = split[4]
    rep = split[3]
    identifier = group+'_'+rep+'_'+pepseq
    NormIntDICT[identifier] = NormInt
    NumPSMsDICT[identifier] = NumPSMs
    if group not in Groups:
        Groups.append(group)

#For Each Peptide + Unique Locus, create 4 possible identifiers (for each group) and check if there are inputs in the dictionaries
PepsExp_rows = PepsExp_data.splitlines()
PepSIQ_Data = list()
for row in PepsExp_rows[1:]:
    row_split = row.split(',')
    pepseq = row_split[0]
    AGI = row_split[8]
    AllAGI = row_split[7]
    NumLoci = row_split[9]
    for group in Groups: #For each pepseq, which Groups are it found in? E.g. only 1CS7wt.
        Sample_AGI_pepseq = group + '|' + AGI + '_' + pepseq
        AGI_pepseq = AGI + '_' + pepseq
        PepLoc = row_split[16]
        Specs_R1 = 0
        Specs_R2 = 0
        Specs_R3 = 0
        PepI_R1 = 0
        PepI_R2 = 0
        PepI_R3 = 0
        if group+'_R1_'+pepseq in NumPSMsDICT.keys():
            Specs_R1 = float(NumPSMsDICT[group+'_R1_'+pepseq])
        if group+'_R2_'+pepseq in NumPSMsDICT.keys():
            Specs_R2 = float(NumPSMsDICT[group+'_R2_'+pepseq])
        if group+'_R3_'+pepseq in NumPSMsDICT.keys():
            Specs_R3 = float(NumPSMsDICT[group+'_R3_'+pepseq])
        if group+'_R1_'+pepseq in NormIntDICT.keys():
            PepI_R1 = float(NormIntDICT[group+'_R1_'+pepseq])
        if group+'_R2_'+pepseq in NormIntDICT.keys():
            PepI_R2 = float(NormIntDICT[group+'_R2_'+pepseq])
        if group+'_R3_'+pepseq in NormIntDICT.keys():
            PepI_R3 = float(NormIntDICT[group+'_R3_'+pepseq])
        Specs = [Specs_R1, Specs_R2, Specs_R3]
        Condition = Specs_R1+Specs_R2+Specs_R3 #Only write an input in PepSIQ if there is >0 PSMs for that peptide!!! 
        if Condition > 0:
            Ordered_list = list()
            Ordered_list.append(Sample_AGI_pepseq)
            Ordered_list.append(group)
            Ordered_list.append(pepseq)
            Ordered_list.append(NumLoci)
            Ordered_list.append(AllAGI)
            Ordered_list.append(AGI)
            Ordered_list.append(AGI_pepseq)
            Ordered_list.append(PepLoc)
            Ordered_list.append(Specs_R1)
            Ordered_list.append(Specs_R2)
            Ordered_list.append(Specs_R3)
            Ordered_list.append(PepI_R1)
            Ordered_list.append(PepI_R2)
            Ordered_list.append(PepI_R3)
            PepSIQ_Data.append(Ordered_list)
        

#Save

Fields = ['SampleGroup|AGI_pepseq','SampleGroup','Pepseq','#Loci','AllAGI','AGI','AGI_pepseq', 'PepLoc','#Specs_R1','#Specs_R2','#Specs_R3','PepI_R1','PepI_R2','PepI_R3']
filename = DatasetName + 'PepSIQ.csv'
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(PepSIQ_Data)