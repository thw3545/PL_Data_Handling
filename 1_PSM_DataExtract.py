"""
First script for processing mass spectrometry data. From Proteome Discoverer, export PMS data as a .txt file
Copy this file into the MS_PDL folder and save it as PSM_rawdata.txt

Ensure you are in the MS_PDL directory. Check the Sysmic Python course for reminder how to navigate the directory on p10-11

IMPORTANT: Set DatasetName now. Otherwise previous DataAnalysis files will be overwritten.

This script will extract the relevant data and save it under Data1Output and Data2Output. This can be cut and pasted into a master Excel sheet"""


#Import

import csv

#Constant

PATH = 'PSM_rawdata.txt'
file1 = open("dsname.txt")
DatasetName = file1.read()
file1.close()

#Import data

with open(PATH, mode='r') as data_file:
    txt_data = data_file.read()

#Split data by line
txt_data_split = txt_data.splitlines()

#Extract data
PSM_List = list()
Data2_List = list()
for PSM in txt_data_split[1:]: #Above split's first item is the list of headings. This cuts out only the values, no headings. 
    untrimmed_PSM_data_list = PSM.split("\t")
    PSM_data_list = list()
    for value in untrimmed_PSM_data_list:
        trimmed_value = value.strip('"')
        PSM_data_list.append(trimmed_value)
    Ordered_list = list()
    Ordered_list2 = list()
    PSM_PeptideID = PSM_data_list[1]
    Annotated_sequence = PSM_data_list[6]
    Annotated_sequence_split = Annotated_sequence.split(".")
    Before = Annotated_sequence_split[0]
    Peptide_sequence = Annotated_sequence_split[1]
    After = Annotated_sequence_split[2]
    Modifications = PSM_data_list[7]
    Intensity = PSM_data_list[22]
    SpectrumFile = PSM_data_list[30]
    Master_protein_accessions = PSM_data_list[9]
    Protein_Accessions = PSM_data_list[10]
    Number_Proteins = PSM_data_list[8]
    SpecFile_Pepseq = SpectrumFile + '#' + Peptide_sequence
    #Load data into ordered list in order of Fields for Data1Output
    Ordered_list.append(PSM_PeptideID)
    Ordered_list.append(Peptide_sequence)
    Ordered_list.append(Annotated_sequence)
    Ordered_list.append(Modifications)
    Ordered_list.append(Intensity)
    Ordered_list.append(SpectrumFile)
    Ordered_list.append(Peptide_sequence)
    Ordered_list.append(Annotated_sequence)
    Ordered_list.append(Before)
    Ordered_list.append(After)
    Ordered_list.append(Master_protein_accessions)
    Ordered_list.append(Protein_Accessions)
    Ordered_list.append(Number_Proteins)
    PSM_List.append(Ordered_list)
    #Load data into ordered list in order of Fields for Data2Output
    Ordered_list2.append(PSM_PeptideID)
    Ordered_list2.append(Peptide_sequence)
    Ordered_list2.append(Annotated_sequence)
    Ordered_list2.append(Modifications)
    Ordered_list2.append(Intensity)
    Ordered_list2.append(SpectrumFile)
    Ordered_list2.append(SpecFile_Pepseq)
    Ordered_list2.append(Intensity)
    Data2_List.append(Ordered_list2)

    

#Save Data as Data1
filename = DatasetName + 'Data1.csv'
Fields = ['PSMs Peptide ID', 'Pepseq', 'Annotated Sequence', 'Modifications', 'Intensity', 'SpectrumFile', 'Pepseq', 'Annotated Sequence', 'Before', 'After', 'Master Protein Accession', 'Protein Accessions','# Proteins']
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(PSM_List)

#Save Data as Data2
filename = DatasetName + 'Data2.csv'
Fields = ['PSMs Peptide ID', 'Pepseq', 'Annotated Sequence', 'Modifications', 'Intensity', 'SpectrumFile', 'SpectrumFile#Pepseq', 'Intensity']
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(Data2_List)
    


