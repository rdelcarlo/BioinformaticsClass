#! /usr/bin/env python3

"""
This script will read through the Bloom_et_al_2018_Reduced_Dataset.csv
This will report the taxon and diadromous category.
This will then sum the log body sizes and print out the total log body sizes for each.
"""

# Create a stylistic line break unit
dash = '-' *47

# Create a variable of the filename
InFileName = "Bloom_etal_2018_Reduced_Dataset.csv"

# Read the InFile
InFile = open(InFileName, 'r')

# Create a starting point variable for row position
Line = 0

# Create a starting point variable for log body size
logbodysize = 0

# Create an empty variable to tally diadromous entries
diad = 0

# Create an empty variable to tally non-diadromous entries
nondiad = 0

# For each line, print out the taxon and diadromous status
for row in InFile:
	if Line > 0:
		row = row.strip('\n')
		row = row.split(',')
		print('{:<32s}{:<15s}'.format(row[0],row[3]))
		size = float(row[1])
		logbodysize = logbodysize + size
		if row[3] == "diadromous":
			diad += 1
		elif row[3] == "non-diadromous":
			nondiad += 1
	else:
		print('\n'+"Taxon"+'\t\t\t\t'+"Diadromous_status"+'\n'+dash)
	Line += 1

print('\n'+dash+'\n'+"Sum Log Body Size"+'\n'+dash+'\n'+str(logbodysize)+'\n')
print(dash+'\n'+"Diadromous  vs  Non-Diadromous"+'\n'+dash+'\n'+str(diad)+'\t\t'+str(nondiad)+'\n')
