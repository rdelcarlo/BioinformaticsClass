#! /usr/bin/env python3

"""
Usage: Python3.7
Create a list of numbers. Then loop through the items in the list adding 1 to every number and print those numbers.
"""

# Create a list of the digits of Pi called, "Pi"
Pi=[3,1,4,1,5,9,2,6,5,3,5,9]
print("Pi = ", Pi)

# Create an empty list to fill with augmented digits of Pi
Rho=[]

# For each item in "Pi", add the value 1 and print
for digit in Pi:
	rho = digit + 1
	Rho.append(rho)

# Print the new list of digits
print("Rho = ",Rho)
