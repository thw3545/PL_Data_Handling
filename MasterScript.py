"""
Before running this programme:

Ensure that AraPort11 fasta sequence is saved as AraPort11_pep.fasta and this is in the current directory.

Ensure that Samples.csv has been filled in as in example (including headers). Note commas in csv separate cells in an excel row. 
Save as csv file

SpectrumFile,NewName,Bait,Biotin,Rep,SampleGroup
20220928_TurnerS_WilsonT_01.raw,1CS7WTb_R1,1CS7WT,b,R1,1CS7WTb
20220928_TurnerS_WilsonT_02.raw,1CS7WTb_R2,1CS7WT,b,R2,1CS7WTb

From ProteomeDiscoverer, export data as PMSs and save as PSM_rawdata.txt
Cells are separated by tabs not commas

"PSMs Workflow ID"	"PSMs Peptide ID"	"Checked"	"Confidence"	"Identifying Node"	"PSM Ambiguity"	"Annotated Sequence"	"Modifications"	"# Proteins"	"Master Protein Accessions"	"Protein Accessions"	"# Missed Cleavages"	"Charge"	"DeltaScore"	"DeltaCn"	"Rank"	"Search Engine Rank"	"m/z [Da]"	"MH+ [Da]"	"Theo. MH+ [Da]"	"DeltaM [ppm]"	"Deltam/z [Da]"	"Intensity"	"Activation Type"	"NCE [%]"	"MS Order"	"Isolation Interference [%]"	"Ion Inject Time [ms]"	"RT [min]"	"First Scan"	"Spectrum File"	"File ID"	"Quan Info"	"XCorr"	"Ions Score"	"# Protein Groups"	"Identity Strict"	"Identity Relaxed"	"Expectation Value"	"Percolator q-Value"	"Percolator PEP"	"Precursor Abundance"	"Apex RT [min]"
"-107"	"11193497"	"False"	"High"	"Mascot (A5)"	"Unambiguous"	"[K].SKDNLYEQKPEEPVPVIPAASPTNDTSAAGSSFASR.[F]"	""	"1"	"AT5G46750.1"	"AT5G46750.1"	"1"	"3"	"1.0000"	"0.0000"	"1"	"1"	"1254.28316"	"3760.83493"	"3760.83005"	"1.30"	"0.00163"	"545911.5"	"HCD"	"30.0"	"MS2"	"40.80803"	"25.000"	"45.5587"	"48301"	"20220928_TurnerS_WilsonT_11.raw"	"F11"	""	""	"57"	"1"	"35.000"	"28.000"	"7.69136217317765E-05"	"2.423E-05"	"1.052E-15"	"483303.125"	"45.51"

You will be asked for a project code. These are used to give output files their unique name. If I give TW-PL-15 files
are saved as e.g. TW-PL-15Data1.csv

"""

import subprocess

program_list = ['Araport11_JSON.py','1_PSM_DataExtract.py', '2_UniqueLociDatabase_Update.py', '3_UniqueLociDatabase_JSON.py', 
'4__PepsDatabase.py','5_Sum Peptides.py', '6_WritePepSIQ.py', '7_WriteProtSIQ.py']

DatasetName = input("Give a Project Code:")
CurrentDate = input("Give the current date as YYYY-MM-DD:")

file = open('dsname.txt', 'w')
file.write(DatasetName)
file.close()
file = open('date.txt', 'w')
file.write(CurrentDate)
file.close()

for program in program_list:
    subprocess.call(['python', program])
    print("Finished:" + program)