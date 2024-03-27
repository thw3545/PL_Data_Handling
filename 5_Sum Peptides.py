"""
For each peptide, there can be multiple PSMs. This script will sum all the PSMs with the same name (e.g. 20220928_TurnerS_WilsonT_02.raw#VKPSSPAELEALmGPK). It will also rename the summed peptide based on
the samples names in Samples.csv. 

The Summed Intensity is normalised. The sum of normalised intensities in a sample is 1E+10. For example, if sum of all spectra in 2E+10, the intensity of each PSM is halved.

Data input: Data 2

Data output: Data 3. This is equivalent to PT1. Note Manoj's PT1 condenses peptides e.g. ImEIASLEK and IMEIASLEK into ImEIASLEK only, summing PSMs and SumInt. This script does not do this. 
"""

#Import

import csv

#Constant

file1 = open("dsname.txt")
DatasetName = file1.read()
file1.close()
PATH = DatasetName + 'Data2.csv'
SamplesPATH = 'Samples.csv'

#Import data

with open(PATH, mode ='r') as datafile:
    Data2_data = datafile.read()
with open(SamplesPATH, mode = 'r') as samplesfile:
    Samples_data = samplesfile.read()

#Extract Sample Names

Samples_rows = Samples_data.splitlines()
SAMPLES = dict() 
for row in Samples_rows:
    split = row.split(',')
    specfile = split[0]
    NewName = split[1]
    Rep = split[4]
    Group = split[5]
    SAMPLES[specfile] = [NewName, Rep, Group] #Convert the specfile name to a meaningful name

#Calculate Normalisation Factor
Data2_rows = Data2_data.splitlines()
TotalIntensityDICT = dict()
for spectra in Data2_rows[1:]:
    split = spectra.split(',')
    intensity = float(split[4])
    specfile = split[5]
    Sample = SAMPLES[specfile][0]
    if Sample not in TotalIntensityDICT.keys():
        TotalIntensityDICT[Sample] = intensity
    else:
        Newvalue = intensity + TotalIntensityDICT[Sample]
        TotalIntensityDICT[Sample] = Newvalue
Normalisation_Factor = dict()
for sample in TotalIntensityDICT.keys():
    SumIntensity = TotalIntensityDICT[sample]
    NormFactor = 1E+10 / SumIntensity
    Normalisation_Factor[sample] = NormFactor

#Sum all Intensities and Rename
PeptideIntensityDICT = dict()
NumPSMs = dict()
for row in Data2_rows[1:]:
    split = row.split(',')
    specfile = split[5]
    intensity = float(split[4])
    pepseq = split[1]
    NewName = SAMPLES[specfile][0] + '_' + pepseq
    if NewName not in PeptideIntensityDICT.keys():
        PeptideIntensityDICT[NewName] = intensity
        NumPSMs[NewName] = 1
    else:
        NewValue = intensity + PeptideIntensityDICT[NewName]
        PeptideIntensityDICT[NewName] = NewValue
        CurrentPSMs = NumPSMs[NewName] + 1
        NumPSMs[NewName] = CurrentPSMs

#Create Output Data
OutputLIST = list()
Occupied_Names = list()
for row in Data2_rows[1:]:
    split = row.split(',')
    specfile = split[5]
    pepseq = split[1]
    sample = SAMPLES[specfile][0]
    Name = sample + '_' + pepseq
    if Name not in Occupied_Names: #There are multiple PSMs in Data2_rows. Thus, need to condense multiple PSMs into a single peptide
        intensity = float(split[4])
        group = SAMPLES[specfile][2]
        rep = SAMPLES[specfile][1]
        SumInt = PeptideIntensityDICT[Name]
        NormInt = SumInt*Normalisation_Factor[sample]
        NumberPSMs = NumPSMs[Name]
        Ordered_list = list()
        Ordered_list.append(Name)
        Ordered_list.append(sample)
        Ordered_list.append(group)
        Ordered_list.append(rep)
        Ordered_list.append(pepseq)
        Ordered_list.append(SumInt)
        Ordered_list.append(NormInt)
        Ordered_list.append(NumberPSMs)
        OutputLIST.append(Ordered_list)
        Occupied_Names.append(Name)

#Save data as Data3
Fields = ['Name','Sample','Group','Rep','Pepseq','SumIntensities','Normalised_Intensity', 'NumPSMs']
filename = DatasetName + 'Data3.csv'
with open(filename, mode='w+', newline='') as csvfile:
    #create a csv writer object
    csvwriter = csv.writer(csvfile)
    #write fields
    csvwriter.writerow(Fields)
    #write the data rows
    csvwriter.writerows(OutputLIST)

