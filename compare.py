#!/usr/bin/env python
# file: compare.py

import string
import sys
import re

def makingList(inFile, outList):
	for hang in inFile:
		hangList = hang.split()
		word = hangList[0]
		if len(word) > 3 and word == "ATOM":
			residue = hangList[3]
			index = hangList[5]
			if len(outList) == eval(index) - 1:
				outList.insert(eval(index) - 1, residue)

def main():

	designList = []
	wtList = []
	
	if sys.argv[1] != '':
		inDesign = open(sys.argv[1], 'r')
		makingList(inDesign, designList)
		inDesign.close()
	else:
		print "No design file"
	
	if sys.argv[2] != '':
		inWT = open(sys.argv[2], 'r')
		makingList(inWT, wtList)
		inWT.close()
	else:
		print "No wildtype file"
	
	if sys.argv[1] != '' and sys.argv[2] != '' and len(designList) == len(wtList):
		outFile = open('diff.txt', 'w')
		totalNum = 0
		for value in range(len(designList)):
			if designList[value] != wtList[value]:
				index = value
				outFile.write("Residue "+str(value+1)+":\tWT: "+wtList[value]+'\t  '+'design: '+designList[value]+'\n')
				totalNum += 1
		outFile.write("\n")
		outFile.write("Total "+str(totalNum)+" residues changed")
		outFile.close()
	elif sys.argv[1] != '' and sys.argv[2] != '' and len(designList) != len(wtList):
		print "Residue numbers are not the same in two files"
		print "File 1: ", len(designList), "residues"
		print "File 2: ", len(wtList), "residues"

main()