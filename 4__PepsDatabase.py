"""

This script uses Data1 and ULDataBase as an input and outputs Peps.csv and Peps_Exp.csv. These can be cut and paste into a Master excel sheet if required.
The AraPort and UniqueLociDatabase JSON Dictionaries are required. Ensure the AraPort_JSON.py and UniqueLociDatabase_JSON.py scripts have been run.

Both Peps and PepsExp do not contain muliple protein accessions for the same locus. Similarly, all duplicates in Data1 are removed.
Peps contains one line per peptide, and multiple AGIs. PepsExp contains one line per AGI, and so peptides with multiple locus AGIs will have multiple lines.

IMPORTANT: Set DatasetName now. Otherwise previous DataAnalysis files will be overwritten.
"""

#Import

import csv
import json

#Constants

file1 = open("dsname.txt")
DatasetName = file1.read()
file1.close()
PATH = DatasetName + 'Data1.csv'
AraPortPATH = 'AraPort11.json'
ULD_PATH = 'UniqueLociDatabase.json'


#Import data

with open(PATH, mode='r') as data_file:
    Data1_data = data_file.read()
with open(AraPortPATH) as json_file:
    AraPort11 = json.load(json_file)
with open(ULD_PATH) as json_file:
    ULDatabase = json.load(json_file)

#Data to Fill
Peps_List = list()
PepsExp_List = list()

#Split data by line

Data1_split = Data1_data.splitlines()

#Calculations for Peps csv - Copying data from Data1
OccupationLIST = list()
for peptide in Data1_split[1:]: #Above split's first item is the list of headings. This cuts out only the values, no headings. 
    peptide_split = peptide.split(',')
    Peptide_seq = peptide_split[6]
    if Peptide_seq not in OccupationLIST: #There is a need to remove duplicates. For each peptide called, the occupation dictionary is checked.
        Annotated_seq = peptide_split[7]
        Before = peptide_split[8]
        After = peptide_split[9]
        Master_ProtAccession = peptide_split[10]
        ProtAccession = peptide_split[11]
        NumProt = peptide_split[12]
        Ordered_list = list()
        Ordered_list.append(Peptide_seq)
        Ordered_list.append(Annotated_seq)
        Ordered_list.append(Before)
        Ordered_list.append(After)
        Ordered_list.append(Master_ProtAccession)
        Ordered_list.append(ProtAccession)
        Ordered_list.append(NumProt)
        AllAGIu = ULDatabase[Peptide_seq]['AllAGI'] #Adding data from ULDatabase. This is the number of Unique Loci
        NumAGI = ULDatabase[Peptide_seq]['NumAGIu']
        if NumAGI == 1:
            PepExclusive = '1_Yes'
        else:
            PepExclusive = '2_No'
        Ordered_list.append(AllAGIu)
        Ordered_list.append(AllAGIu)
        Ordered_list.append(NumAGI)
        Ordered_list.append(PepExclusive)
        Peps_List.append(Ordered_list)
        OccupationLIST.append(Peptide_seq)

#Save Data as Peps.csv
filename = DatasetName + 'Peps.csv'
Fields = ['Pepseq', 'Annotated Sequence', 'Before', 'After', 'Master Protein Accession', 'Protein Accessions','# Proteins', 'AllAGIu','AGI','#AGI','PepExclusive_yn']
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(Peps_List)

#Calculations for Peps_Exp
for peptide in Peps_List: 
    if len(peptide[8]) == 11: #Peptides with only one associated protein accession. This contains 11 characters
        AGI = peptide[8]
        locus = AGI[0:9]
        fasta = '>'+AGI
        ProteinSeq = AraPort11[fasta].strip('*')
        ProteinLen = len(ProteinSeq)
        AGI_PepSeq = AGI+'_'+peptide[0]
        PepLoc = ProteinSeq.find(peptide[0].upper()) + 1 #Peptides can contain lower case m. +1 Needed as Python starts counting at 0
        peptide.append(locus)
        peptide.append(fasta)
        peptide.append(ProteinSeq)
        peptide.append(ProteinLen)
        peptide.append(AGI_PepSeq)
        peptide.append(PepLoc)
        PepsExp_List.append(peptide)
    else:
        split_AGIus = peptide[8].split('; ') #How many AGIus are there? This is the number of copies I need to make (Expansion)
        numSplitAGIs = len(split_AGIus)
        for AGI in split_AGIus:
            peptide_copy = peptide.copy() #Makes a copy for each AGI, and replaces the original AGI value (used to be multiple accessions) with a single AGI.
            peptide_copy[8] = AGI
            locus = AGI[0:9]
            fasta = '>'+AGI
            ProteinSeq = AraPort11[fasta].strip('*') #Remove the STOP *
            ProteinLen = len(ProteinSeq)
            AGI_PepSeq = AGI+'_'+peptide_copy[0]
            PepLoc = ProteinSeq.find(peptide_copy[0].upper()) + 1
            peptide_copy.append(locus)
            peptide_copy.append(fasta)
            peptide_copy.append(ProteinSeq)
            peptide_copy.append(ProteinLen)
            peptide_copy.append(AGI_PepSeq)
            peptide_copy.append(PepLoc)
            PepsExp_List.append(peptide_copy)

#Save Data as Peps_Exp.csv
filename = DatasetName + 'Peps_Exp.csv'
Fields = ['Pepseq', 'Annotated Sequence', 'Before', 'After', 'Master Protein Accession', 'Protein Accessions','# Proteins', 'AllAGIu','AGI','#AGI','PepExclusive_yn', 'Locus', 'FASTA', 'ProteinSeq', 'ProteinLen','AGI_Pepseq','PepLoc']
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(PepsExp_List)


