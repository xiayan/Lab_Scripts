#!/usr/bin/env python
# file: extract.py

import string
import sys
import re

def main():

	designList = []
	wtList = []
	
	if sys.argv[1] != '':
		inDesign = open(sys.argv[1], 'r')
		for hang in inDesign:
			hangList = hang.split()
			word = hangList[0]
			if len(word) > 3 and word[3] == '_':
				designList.append(hangList[-1])
		inDesign.close()
	else:
		print "No design file"
	
	if sys.argv[2] != '':
		inWT = open(sys.argv[2], 'r')
		for hang in inWT:
			hangList = hang.split()
			word = hangList[0]
			if len(word) > 3 and word[3] == "_":
				wtList.append(hangList[-1])
		inWT.close()
	else:
		print "No wildtype file"
	
	if sys.argv[1] != '' and sys.argv[2] != '' and len(designList) == len(wtList):
		outFile = open('diff.txt', 'w')
		for value in range(len(designList)):
			designValue = eval(designList[value])
			wtValue = eval(wtList[value])
			diff = designValue - wtValue
			
			#outFile.write(str(diff)+'\n')
			outFile.write(str(value+1)+'\t'+str(diff)+'\n')
		
		outFile.close()
	elif sys.argv[1] != '' and sys.argv[2] != '' and len(designList) != len(wtList):
		print "Residue numbers are not the same in two files"

main()
