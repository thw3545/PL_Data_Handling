"""
A list of Pepseq, AGIu_ALL, NumAGI and DataAdded csv file is then converted into a JSON Dictionary, first input = pepseq, second input is 'AllAGI' or 'NumAGIu'. Output is value of second input.

This dataset contains only one splice isoform for each protein. 

Note if there are multiple AGIu_ALL, this script accounts for it. """

#Import

import json

#Constants

PATH = 'UniqueLociDatabase.csv'

#Import data

with open(PATH, mode = 'r') as data_file:
    ULDatabase = data_file.read()

#Save updated ULDatabase as dictionary
DICT = dict()
ULDatabase_split = ULDatabase.split('\n')
ULDatabase_split = ULDatabase.split('\n')
for peptide in ULDatabase_split[1:]:
    peptide_split = peptide.split(',')
    if len(peptide_split) > 1: #The final row of the csv file (which is just empty) can cause an error to occur with peptide_split. This removes it
        pepseq = peptide_split[0]
        AGIu_All = peptide_split[1]
        NumAGIu = peptide_split[2]
        DICT[pepseq] = dict()
        DICT[pepseq]['NumAGIu'] = NumAGIu
        DICT[pepseq]['AllAGI'] = AGIu_All

#Save dictionary to current directory as .json file
with open('UniqueLociDatabase.json', 'w') as dct:
    json.dump(DICT, dct)