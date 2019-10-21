#! /usr/bin/env python3

"""
Usage: Python
Indication: Will decide if the animals in Sizes_dict are "Big" or "small"
"""
# Create a linebreak variable
N="\n"

# Create a dictionary of animal sizes, Sizes_dict[“Animal”]=size
Sizes_dict={
'Fly':0.5,
'Roach':1.0,
'Taranchula':10.0,
'Garter Snake':19.0,
'Vole':45.0,
'Mouse':70.0,
'Cat':2200.0,
'Dog':44000.0}

print(N,"The dictionary of animal sizes is: ",N,Sizes_dict)

# From the dictionary Sizes_dict, create a list of the keys.
Keys = list(Sizes_dict.keys())

# From the dictionary Sizes_dict, create a list of the values.
Values = list(Sizes_dict.values())

# Create an empty list to print animal sizes
Big_or_small = []

# For each animal in the list, decide if the animal is big or small
for size in Values:
	if size >= 20:
		decision = "Big"
	else:
		decision = "small"
	Big_or_small.append(decision)

# Create an integer list the same length as the lists above.
length = range(8)

# Create an empty dictionary to populate with the new size determinations
Decision = {}

# For each item of the lists, pair with the decision of the previous for loop
for each in length:
	Decision[Keys[each]] = Big_or_small[each]

# Print the decision criteria.
print(N, "If the animal mass is greater than or equal to 20.0g, it is a Big animal, otherwise it is small.")

# Print the animal size list
print(N, "The new dictionary is: ", N, Decision, N)


