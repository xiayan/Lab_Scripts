#!/usr/bin/python

import os 
import sys
import time
from ProgressBar import *

def download_pdb(pdb_id):
    url = 'http://www.rcsb.org/pdb/files/%s.pdb' % (pdb_id)
    
    outName = pdb_id + ".pdb"
    
    command = "curl -silent " + url + " > " + outName
    os.system(command)

def main():
    assert(len(sys.argv) > 2)
    pdbList = sys.argv[1]
    dest = sys.argv[2]
    
    path = os.getcwd()
    newPath = os.path.abspath(dest)
    os.chdir(newPath)
    
    aList = open(pdbList, 'r')
    
    aList = [pdb for pdb in aList if not pdb == "\n"];
    totalNumber = float(len(aList))
    counterNumber = 0
    
    runningTime = time.time()
    
    for filename in aList:
        filename = filename.rstrip()
        download_pdb(filename)
        counterNumber = counterNumber + 1
        progress(30, float(counterNumber / totalNumber * 100))
        
    runningTime = time.time() - runningTime
    print ("Total Time: ", runningTime, "sec")
    
    os.chdir(path)
        
if __name__ == "__main__": main()
