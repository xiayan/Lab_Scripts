#!/usr/bin/python2.5

from rosetta import *
from math import *
import sys, os

def main():

    path = os.getcwd()
    dirContents = os.listdir(path)
    
    # write c-n bond length to outfile
    outfile = open("data.txt", 'w')
    
    rosetta.init()
    # process each pdb file under the current working directory
    for pdb in dirContents:
        if pdb.endswith(".pdb") and os.path.getsize(pdb) != 0:
            try:
                pose = Pose(pdb);
                print "processing " + pdb
                #calculate the c-n bond length for each residue
                for i in range(1, pose.total_residue()+1):
                    Nitrogen = pose.residue(i).xyz(1)
                    CAlpha = pose.residue(i).xyz(2)
                    N_CA_vector = CAlpha - Nitrogen
                    distance = N_CA_vector.norm
                    outfile.write(str(distance) + "\n")
            except Exception:
                print sys.exc_info()
                continue
            else:
                print "Caught!\n"
                continue
    
    outfile.close()
    print "Done"

if __name__ == "__main__": main()
