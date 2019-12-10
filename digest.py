#! /usr/bin/env python3

# digest.py -- version 1.0
# This code will read an input amino acid sequence and calculate its molecular weight based on the
# dictionary AminoDict pulled from http://practicalcomputing.org/aminoacid.html
# This will then take the sequence and cut it AFTER R & K for Trypsin
# Then BEFORE N for Asparginase (AspN)
# This will then calculate the mass of each fragment for the single digest and for the double digest
# This will then print the charge of each fragment under acidic conditions (pH ~ 2.7, 0.1% Formic Acid)
# It is worth noting that at pH 2.7, only three amino acids (KHR) carry a charge (+3.0)
# However, additionally, it is believed that at pH 2.7, the backbone carries a delocalized charge of +0.7
# Therefore, a peptide of 3 amino acids, KHR, would carry a charge of +3.7
# This is the charge in "elementary charges" - the exact value of an elementary charge is 1.602176634×10(−19) Coulomb
# The charge to mass ratio of each fragment will then be calculated and displayed.
# Of this population of fragments, a final report will show those which carry a positive charge and are between 7 and 20 amino acids long.
# It will also show those which do not have a positive charge, but are within the size range.
# usage: This can be customized for any user input sequence (protein fasta) by enter a single line amino acid sequence between quotes in ProteinSeq. Save document, 
# then run by calling ./digest.py
# However, the current version is tailored to Sequences of NaV1.4
# This script can be used on any sequence file; .fasta; .txt, or manual user input.
# The demo file coming with this file is 'hnav14.fasta' and represents the sequence of human NaV1.4
# If the demo file hnav14.fasta is not present or was not downloaded, the first input and 'ProteinSeq' definitions can be commented out and the full sequence 
# of Human NaV1.4 is hard coded into this file for demonstrative purposes.


import re

N = "\n"
L = "-" * 87


# This dictionary defines, in atomic mass units (AMU) or Daltons (D)
AminoDict = {
'A':89.09,
'R':174.20,
'N':132.12,
'D':133.10,
'C':121.15,
'Q':146.15,
'E':147.13,
'G':75.07,
'H':155.16,
'I':131.17,
'L':131.17,
'K':146.19,
'M':149.21,
'F':165.19,
'P':115.13,
'S':105.09,
'T':119.12,
'W':204.23,
'Y':181.19,
'V':117.15,
'X':0.0,
'-':0.0,
'*':0.0
}

# This Dictionary defines, in coulombs (C), the charge of the amino acids in a peptide at pH = 2.7 (formic acid environment)
Qdict = {
'K':1.0,
'H':1.0,
'R':1.0,
'A':0.0,
'N':0.0,
'D':0.0,
'C':0.0,
'Q':0.0,
'E':0.0,
'G':0.0,
'I':0.0,
'L':0.0,
'M':0.0,
'F':0.0,
'P':0.0,
'S':0.0,
'T':0.0,
'W':0.0,
'Y':0.0,
'V':0.0,
'X':0.0,
'-':0.0,
'*':0.0
}

# Create variables of NaV1.4 sequences
# ProteinSeq = Ths NaV1.4 +
# ProteinSeq = Ths NaV1.4 LVNV
# ProteinSeq = Hs  NaV1.4 +

# Improve the versatility of this script by allowing for input rather than hard-coded sequence.
infilename = input("Please enter a FASTA formatted filename to read in the sequence...")
seq = open(infilename, 'r')
sequ = seq.read()
string = re.search('>\S+\n(\S+)', sequ)
ProteinSeq = string.group(1)

# This is the sequence that will be used for the analysis.
#ProteinSeq = str("MARPSLCTLVPLGPECLRPFTRESLAAIEQRAVEEEARLQRNKQMEIEEPERKPRSDLEAGKNLPMIYGDPPPEVIGIPLEDLDPYYSNKKTFIVLNKGKAIFRFSATPALYLLSPFSVVRRGAIKVLIHALFSMFIMITILTNCVFMTMSDPPPWSKNVEYTFTGIYTFESLIKILARGFCVDDFTFLRDPWNWLDFSVIMMAYLTEFVDLGNISALRTFRVLRALKTITVIPGLKTIVGALIQSVKKLSDVMILTVFCLSVFALVGLQLFMGNLRQKCVRWPPPFNDTNTTWYSNDTWYGNDTWYGNEMWYGNDSWYANDTWNSHASWATNDTFDWDAYISDEGNFYFLEGSNDALLCGNSSDAGHCPEGYECIKTGRNPNYGYTSYDTFSWAFLALFRLMTQDYWENLFQLTLRAAGKTYMIFFVVIIFLGSFYLINLILAVVAMAYAEQNEATLAEDKEKEEEFQQMLEKFKKHQEELEKAKAAQALEGGEADGDPAHGKDCNGSLDTSQGEKGAPRQSSSGDSGISDAMEELEEAHQKCPPWWYKCAHKVLIWNCCAPWLKFKNIIHLIVMDPFVDLGITICIVLNTLFMAMEHYPMTEHFDNVLTVGNLVFTGIFTAEMVLKLIAMDPYEYFQQGWNIFDSIIVTLSLVELGLANVQGLSVLRSFRLLRVFKLAKSWPTLNMLIKIIGNSVGALGNLTLVLAIIVFIFAVVGMQLFGKSYKECVCKIALDCNLPRWHMHDFFHSFLIVFRILCGEWIETMWDCMEVAGQAMCLTVFLMVMVIGNLVVLNLFLALLLSSFSADSLAASDEDGEMNNLQIAIGRIKLGIGFAKAFLLGLLHGKILSPKDIMLSLGEADGAGEAGEAGETAPEDEKKEPPEEDLKKDNHILNHMGLADGPPSSLELDHLNFINNPYLTIQVPIASEESDLEMPTEEETDTFSEPEDSKKPPQPLYDGNSSVCSTADYKPPEEDPEEQAEENPEGEQPEECFTEACVQRWPCLYVDISQGRGKKWWTLRRACFKIVEHNWFETFIVFMILLSSGALAFEDIYIEQRRVIRTILEYADKVFTYIFIMEMLLKWVAYGFKVYFTNAWCWLDFLIVDVSIISLVANWLGYSELGPIKSLRTLRALRPLRALSRFEGMRVVVNALLGAIPSIMNVLLVCLIFWLIFSIMGVNLFAGKFYYCINTTTSERFDISEVNNKSECESLMHTGQVRWLNVKVNYDNVGLGYLSLLQVATFKGWMDIMYAAVDSREKEEQPQYEVNLYMYLYFVIFIIFGSFFTLNLFIGVIIDNFNQQKKKLGGKDIFMTEEQKKYYNAMKKLGSKKPQKPIPRPQNKIQGMVYDLVTKQAFDITIMILICLNMVTMMVETDNQSQLKVDILYNINMIFIIIFTGECVLKMLALRQYYFTVGWNIFDFVVVILSIVGLALSDLIQKYFVSPTLFRVIRLARIGRVLRLIRGAKGIRTLLFALMMSLPALFNIGLLLFLVMFIYSIFGMSNFAYVKKESGIDDMFNFETFGNSIICLFEITTSAGWDGLLNPILNSGPPDCDPNLENPGTSVKGDCGNPSIGICFFCSYIIISFLIVVNMYIAIILENFNVATEESSEPLGEDDFEMFYETWEKFDPDATQFIAYSRLSDFVDTLQEPLRIAKPNKIKLITLDLPMVPGDKIHCLDILFALTKEVLGDSGEMDALKQTMEEKFMAANPSKVSYEPITTTLKRKHEEVCAIKIQRAYRRHLLQRSMKQASYMYRHSHDGSGDDAPEKEGLLANTMSKMYGHENGNSSSPSPEEKGEAGDAGPTMGLMPISPSDTAWPPAPPPGQTVRPGVKESLV")
#ProteinSeq = input("Enter a peptide sequence: ")

ProteinSeq.replace(' ','')
MolWeight = float(0.0)

for AminoAcid in ProteinSeq:
	MolWeight = MolWeight + AminoDict[AminoAcid]

print(N)
input("Press enter to display the input protein sequence..."+N)
print("Protein: ", ProteinSeq, N)
input("Press enter to calculate the molecular mass of the input protein..."+N)
if MolWeight > 1000:
	Unit = "kD"
	print("Molecular Weight: %.1f %s" % (MolWeight/1000,Unit) + N)
elif MolWeight <= 1000:
	Unit = "D"
	print("Molecular Weight: %.1f %s" % (MolWeight,Unit) + N)

# Take the protein sequence and read for the reqular expression of trypsin cut sites (R & K)

Trp = re.split('(R|K)',ProteinSeq)
TrpRK = []
frag = int(0)

input("Press enter to digest the input sequence with Trypsin. Trypsin will digest the protein at arginine (R+) and lysine (K+), resulting in the following fragments: "+N)


# The re.split removes the delimiting AA; the actual fragment will have it; make a list which concatenates every two items
if frag == (len(Trp) - 1):
	TrpRK.append(Trp[-1])
elif frag <= (len(Trp)-3):
	for fragment in Trp:
		ment = int()
		if frag <= (len(Trp)-3):
			ment = frag + int(1)
			digest = Trp[frag] + Trp[ment]
		elif frag >= (len(Trp)-3):
			digest = Trp[frag]
		TrpRK.append(digest)
		if frag <= (len(Trp)-2):
			frag += 2
		elif frag >= (len(Trp)-2):
			break
print(TrpRK,N)

# Count the mass of the amino acids in each fragment using AminoDict
# Append Take your TrpRK [] list and append each row with the above parameters
# Sort said list by fragment length
# For fragments of 7 < length < 21, report the fragment sequence and charge to mass ratio

fragmass = []
fragcharge = []
mz = []
zm = []

input("Press enter to calculate the mass, charge, and respective ratios of the above fragments:"+N)

for fragment in TrpRK:
	#print(fragment)
	FragmentMass = float(0.0)
	FragmentCharge = float(0.0)
	# Count the mass of each fragment
	for residue in fragment:
		FragmentMass = FragmentMass + AminoDict[residue]
	fragmass.append(round(FragmentMass,2))
	# Count the charge of each fragment at pH 2.7 using Qdict
	for residue in fragment:
		FragmentCharge = FragmentCharge + Qdict[residue]
	FragmentCharge = FragmentCharge + 0.7
	fragcharge.append(FragmentCharge)
	mz.append(FragmentMass/FragmentCharge)
	zm.append(FragmentCharge/FragmentMass)
	#print("Fragment Mass: %.2f" % FragmentMass)
	#print("Fragment Charge: %.1f" % FragmentCharge)
	# Calculate the charge to mass ratio of each fragment
	#print("Fragment Charge to Mass Ratio: %.5f x 10^-3" % (FragmentCharge/FragmentMass*1000))
	# Calculate the mass to charge ratio (m/z)
	#print("Fragment Mass to Charge Ratio: %.5f" % (FragmentMass/FragmentCharge))
#print(fragmass)
#print(fragcharge)
#print(mz)
#print(zm)

singledigest = []
print(L+N+"Fragment\t\t\tMass\t\tCharge\t\tmz\t\tzm"+N+L+N)
index=0
for i in TrpRK:
	list = []
	list.append(TrpRK[index])
	list.append(round(fragmass[index],2))
	list.append(fragcharge[index])
	list.append(mz[index])
	list.append(zm[index])
	#list.append('\n')
	singledigest.append(list)
	print("%s" % (TrpRK[index]))
	print("\t\t\t\t%.2f\t\t%.2f\t\t%.2f\t\t%.5f" % (fragmass[index],fragcharge[index],mz[index],zm[index]))
	index += 1
#print(singledigest)
print(N)
singledigest = sorted(singledigest, key=lambda x: len(x[0]))
TrypDigest = []
for list in singledigest:
	if len(list[0]) >= 7:
		if len(list[0]) <= 20:
			TrypDigest.append(list)
#print("The fragments of volatile size (7-20AA) are as follows:")
#print(TrypDigest)
#print(N)

input("Press enter to report the most probable volatile peptides. Peptides which are most likely to fly will generally be 7 to 25 amino acids in length and carry a native charge greater than two. Singly charged peptides will be included in the output."+N)

# Report Volatile Peptides as a table
TrypDigest = sorted(TrypDigest, key=lambda x: x[2])
TrypDigest = sorted(TrypDigest, key=lambda x: x[3])
TrypVolDigest = []
TrypVolDigestbetter = []
for list in TrypDigest:
	if list[3] <= 390:
		TrypVolDigest.append(list)
	elif list[3] > 867:
		TrypVolDigest.append(list)
	elif list[3] >= 390:
		if len(list[0]) <= 867:
			TrypVolDigestbetter.append(list)

print(L+N+"Fragment\t\t\tMass\t\tCharge\t\tmz\t\tzm"+N+L+N)
for each in TrypVolDigestbetter:
        print("%s" % (each[0]))
        print("\t\t\t\t%.2f\t\t%.2f\t\t%.2f\t\t%.5f" % (each[1],each[2],each[3],each[4]))
print(L+N+"Fragment\t\t\tMass\t\tCharge\t\tmz\t\tzm"+N+L+N)

################ TRIPLE DIGEST ####################


# Create a double digest output for AspN & Tryp, cutting at D, R+ & K+. Remember AspN cuts BEFORE (n-terminally) to D)
# First take the input sequence, ProteinSeq, and again cut by R & K and reassemble the fragments to have the terminal AA.
input("Press enter to digest the input sequence by both Trypsin & Aspartic Acid Endopeptidase (AspN)..."+N)

# Create an empty list to contain the result of the subsequent digest results.
TripleDigest = []

# Create a zero variable for looping through lists of TrpRK items delimited by D
listindex = 0

# Work through each item in TrpRK. If "D" is found in this item, parse it by D.
# The parsed items will need to be rejoined: Real Fragment = D + Subsequent Fragment
for each in TrpRK:
	if listindex == len(TrpRK)-1:
		TripleDigest.append(TrpRK[-1])
	elif listindex <= len(TrpRK)-1:
		if "D" in TrpRK[listindex]:
			Dcut = re.split('(D)',TrpRK[listindex])
			# Create a zero variable for looping through Dcut list
			fragindex = 0
			for each in Dcut:
				if 'D' in Dcut[fragindex]:
					TripleDigest.append(Dcut[fragindex]+Dcut[fragindex+1])
					Dcut.remove(Dcut[fragindex+1])
					Dcut.remove(Dcut[fragindex])
				elif 'D' not in Dcut[fragindex]:
					TripleDigest.append(Dcut[fragindex])
					fragindex += 1
		elif "D" not in TrpRK[listindex]:
			TripleDigest.append(TrpRK[listindex])
	listindex += 1
while '' in TripleDigest:
	TripleDigest.remove('')
print(TripleDigest,N)

# Calculate the mass of the amino acids in each fragment using AminoDict
# Append the DRK[] list and append each row with the above parameters
# Sort said list by mass-to-charge ratio and then by fragment length
# For fragments of 7 < length < 21, report the fragment sequence and charge to mass ratio

fragmassDRK = []
fragchargeDRK = []
mzDRK = []
zmDRK = []

for fragment in TripleDigest:
	FragmentMass = float(0.0)
	FragmentCharge = float(0.0)
	# Count the mass of each fragment
	for residue in fragment:
		FragmentMass = FragmentMass + AminoDict[residue]
	fragmassDRK.append(round(FragmentMass,2))
	# Count the charge of each fragment at pH 2.7 using Qdict
	for residue in fragment:
		FragmentCharge = FragmentCharge + Qdict[residue]
	FragmentCharge = FragmentCharge + 0.7
	fragchargeDRK.append(FragmentCharge)
	mzDRK.append(FragmentMass/FragmentCharge)
	zmDRK.append(FragmentCharge/FragmentMass)
#print(fragmassDRK)
#print(fragchargeDRK)
#print(mzDRK)
#print(zmDRK)

input("Press enter to see a list of the most probable volatile peptides when digested with Tryp & AspN"+N)

DRK = []
indice = 0
for i in TripleDigest:
	list = []
	list.append(TripleDigest[indice])
	list.append(round(fragmassDRK[indice],2))
	list.append(fragchargeDRK[indice])
	list.append(mzDRK[indice])
	list.append(zmDRK[indice])
	DRK.append(list)
	indice += 1

# Report Volatile Double-Digest Peptides as a table
DRK = sorted(DRK, key=lambda x: len(x[0]))
DRK = sorted(DRK, key=lambda x: x[2])
DRK = sorted(DRK, key=lambda x: x[3])
DRKv = []
for list in DRK:
	if len(list[0]) >= 7:
		if len(list[0]) <=20:
			DRKv.append(list)
DRKvmz = []
for list in DRKv:
	if list[3] >= 390:
		if list[3] <= 867:
			DRKvmz.append(list)
print(L+N+"Fragment\t\t\tMass\t\tCharge\t\tmz\t\tzm"+N+L+N)
for each in DRKvmz:
	print("%s" % (each[0]))
	print("\t\t\t\t%.2f\t\t%.2f\t\t%.2f\t\t%.5f" % (each[1],each[2],each[3],each[4]))
print(L+N+"Fragment\t\t\tMass\t\tCharge\t\tmz\t\tzm"+N+L+N)


## To improve this script, introduce an optimization routine wherein one can give an input sequence and get out what amino acids should be used as
## cut sites so as to see a targeted fragment of the protein by ensuring it ends up in a fragment of optimal mz (390 - 900)
