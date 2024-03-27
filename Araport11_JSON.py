"""
With downloading the AraPort11 Proteome, the file (GZ) was unzipped with 7-Zip and saved under fasta format. This script makes a JSON dictionary
from the fasta file. The input fasta key e.g. >AT5G46750.1 returns the Protein Peptide sequence"""

#Import

import json

#Constants

PATH = 'Araport11_pep.fasta'

#Import data

with open(PATH, mode = 'r') as data_file:
    AraPort11 = data_file.read()

#Extract data
DICT = dict()
AraPort11_split = AraPort11.split('>')
for fasta in AraPort11_split[1:]:
    Name = '>' + fasta[0:11]
    tabs = fasta.splitlines()
    sequence = ''.join(tabs[1:])
    DICT[Name] = sequence
#Save dictionary to current directory as .json file
with open('AraPort11.json', 'w') as dct:
    json.dump(DICT, dct)

