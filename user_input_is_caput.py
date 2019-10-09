#! /usr/bin/env python3

"""
	This code will take a user input sentence and convert it to a concatenated, lowercase string.
	This code will then count the length of this string in characters.
	usage: run on python3
"""

N= "\n"

print(N)
#The sentence comes from a user input:
Sentence = input("Enter a sentence which you would like concatenated and counted: ")
Sentence = Sentence.lower()
Sentence = Sentence.replace(" ","")
Length=len(Sentence)
print(N)
print("The sentence is composed of %d non-white-space characters." % (Length))
print(N)
print("This is the length of your input: ",N)
print(Sentence,N)
print("If you would like a sample sentence to try, give this a go: ",N)
print("2019 Nobel Prize in Chemistry goes to John B. Goodenough. I guess he do be good enough. (He is now the world's oldest Laureate). (And to M. Stanley Whittingham & Akira Yoshino, all for lithium ion batteries.)")
