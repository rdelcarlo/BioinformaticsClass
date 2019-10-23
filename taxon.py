#! /usr/bin/env python3

"""
This script will read through the Bloom_et_al_2018_Reduced_Dataset.csv
This will report the taxon and diadromous category.
This will then sum the log body sizes and print out the total log body sizes for each.
"""

# Import the regular expression profiling
import re

# Create a variable of the filename
InFileName = "Bloom_etal_2018_Reduced_Dataset.csv"

# Read the InFile
InFile = open(InFileName, 'r')

# Create a starting point variable for row position
Line = 0

# Create a starting point variable for log body size
logbodysize = 0

# Create a stylistic line break unit
dash = '-' *47

# For each line, print out the taxon and diadromous status
for row in InFile:
	if Line > 0:
		row = row.strip('\n')
		row = row.split(',')
		print('{:<32s}{:<15s}'.format(row[0],row[3]))
		size = float(row[1])
		logbodysize = logbodysize + size
	else:
		print('\n'+"Taxon"+'\t\t\t\t'+"Diadromous_status"+'\n'+dash)
	Line += 1

print('\n'+dash+'\n'+"Sum Log Body Size"+'\n'+dash+'\n'+str(logbodysize)+'\n')
