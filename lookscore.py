#!/usr/bin/env python
# file: lookscore.py

import string
import sys

def main():

	compareList = []
	nameList = []
	
	if sys.argv[1] != '':
		inDesign = open(sys.argv[1], 'r')
		
		for hang in inDesign:
			hangList = hang.split()
			if len(hangList) > 3:
				compareList.append(hangList[1])
				nameList.append(hangList[-1])
		inDesign.close()
	else:
		print "No score file"
	
	compareList.pop(0)
	nameList.pop(0)
	
	if sys.argv[1] != '':
		outFile = open('list.txt', 'w')
		score = compareList[0]
		for value in compareList:
			iScore = eval(value)
			if iScore < score:
				score = iScore
		for i in [i for i, value in enumerate(compareList) if eval(value) == score]:
			print str(i+1), '\t', str(score)
			outFile.write(nameList[i]+'.pdb'+'\n')
		
		outFile.close()
		
main()
