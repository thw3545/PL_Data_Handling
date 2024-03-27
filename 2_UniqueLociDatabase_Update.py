"""
First, the new list of Peptides and associated AGIs is loaded into the UniqueLociDatabase.csv file.

A list of Pepseq, AGIu_ALL, NumAGI and DataAdded csv file is then converted into a JSON Dictionary, first input = pepseq, second input is 'AllAGI' or 'NumAGIu'. Output is value of second input.

This dataset contains only one splice isoform for each protein. 

Note if there are multiple AGIu_ALL, this script accounts for it. """

#Import

import csv

#Constants

file1 = open("dsname.txt")
DatasetName = file1.read()
file1.close()
PATH = 'UniqueLociDatabase.csv'
Data1PATH = DatasetName + 'Data1.csv'
file1 = open("date.txt")
CurrentDate = file1.read()
file1.close()

#Import data

with open(PATH, mode = 'r') as data_file:
    ULDatabase = data_file.read()
with open(Data1PATH, mode='r') as data_file:
    Data1_data = data_file.read()

#List current Peptides in ULDatabase

ULDatabase_split = ULDatabase.split('\n')
Current_ULD_peps = list()
for peptide in ULDatabase_split[1:]:
    peptide_split = peptide.split(',')
    pepseq = peptide_split[0]
    Current_ULD_peps.append(pepseq)



#Add Peptides from Data1 into ULDatabase. Condenses AGIs to lowest index for each locus (one splice isoform per protein)
NewData1Peptides = list()
Data1_lines = Data1_data.splitlines()
for peptide in Data1_lines:
    peptide_split = peptide.split(',')
    pepseq = peptide_split[1]
    if pepseq not in Current_ULD_peps: #Only peptides not currently in Database
        Current_ULD_peps.append(pepseq) #There are duplicates in the Data1 set. This prevents a duplicate from being added
        ProteinAccessions = peptide_split[11]
        NumProteinAccessions = len(ProteinAccessions.split(';'))
        if NumProteinAccessions == 1: #This peptide has only one protein. No need to modify ProteinAccessions
            Ordered_list=list()
            Ordered_list.append(pepseq)
            Ordered_list.append(ProteinAccessions)
            Ordered_list.append(1)
            Ordered_list.append(CurrentDate)
            NewData1Peptides.append(Ordered_list)
        else: #this peptide has multiple proteins. Need to select lowest AGI index for each Locus
            AGIs = ProteinAccessions.split(';')
            AGI_all = dict() #Contains all loci, but only one AGI per locus
            for AGI in AGIs:
                agi = AGI.strip(' ')
                AGI_Locus = agi[0:9]
                AGI_index = agi[10]
                if AGI_Locus not in AGI_all.keys():
                    AGI_all[AGI_Locus] = int(AGI_index)
                elif AGI_all[AGI_Locus] > int(AGI_index):
                    AGI_all[AGI_Locus] = int(AGI_index)
            Ordered_list=list()
            Ordered_list.append(pepseq)
            AGIu = str()
            for key in AGI_all.keys():
                agi = key + '.' + str(AGI_all[key]) + '; '
                AGIu = AGIu + agi
            AGIu = AGIu.strip('; ')
            Ordered_list.append(AGIu)
            NumAGI = len(AGIu.split(';'))
            Ordered_list.append(NumAGI)
            Ordered_list.append(CurrentDate)
            NewData1Peptides.append(Ordered_list)

#Append Database with new peptides
with open(PATH, mode = 'a', newline = '') as data_file:
    #create a csv writer object
    csvwriter = csv.writer(data_file)
    #write the data rows
    csvwriter.writerows(NewData1Peptides)

