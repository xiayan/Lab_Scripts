#!/Library/Frameworks/Python.framework/Versions/3.2/bin/python3.2

import sys
import os
import math
from ProgressBar import *
import time
def clean(aFile, outfile):
    for line in aFile:
        lineLength = len(line)
        if lineLength > 4 and line[0:4] == "ATOM":
            outfile.write(line)

def main():
    
    startTime = time.time()
    
    path = os.getcwd()
    aList = os.listdir(path)
    
    aList = [pdb for pdb in aList if pdb.endswith(".pdb")];
    totalNumber = float(len(aList))
    currentNumber = 0
    
    for molecule in aList:
        aFile = open(molecule, 'r')
        cleanName = molecule[:-4] + "_clean.pdb";
        outfile = open(cleanName, 'w')
            
        clean(aFile, outfile)
                
        aFile.close()
        outfile.close()
    
        currentNumber = currentNumber + 1
        progress(30, float(currentNumber / totalNumber * 100))
        
    endTime = time.time()
    print (str(endTime - startTime), "seconds.")
    
if __name__ == "__main__": main() 
