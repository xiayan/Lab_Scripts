#!/usr/bin/python

import os, sys
from pymol import *

def yxOpenPDB(pdbName='none', show=True):
    
    if pdbName == "none":
        print "pdb code is required"
        return
    else:
        path = os.environ['HOME'] + '/Documents/PDB/'
        if not os.path.exists(path):
            os.makedirs(path)
            
        os.chdir(path)
        
        pdbName = pdbName.upper() + '.pdb'
        fileList = os.listdir(path)
    
        if not (pdbName in fileList):
            url = 'http://www.rcsb.org/pdb/files/%s' % pdbName
            command = "curl -silent " + url + " > " + pdbName
            os.system(command)
            
            firstline = open(pdbName, 'r').readline().rstrip()
            
            if (firstline == "HTTP/1.1 404 Not Found") or (firstline == "HTTP/1.1 302 Moved Temporarily"):
                print "No PDB found from RCSB"
                os.remove(pdbName)
                return
            else:
                print "Fetched from RCSB"
            
        else:
            print "Exists at", path
        
    if show:
        cmd.load(pdbName)
        cmd.hide('everything')
        cmd.show('cartoon')
    
	cmd.hide('everything', 'hydrogens')
    
cmd.extend('openPDB', yxOpenPDB)

def main():
    assert( len(sys.argv) > 1)
    
    yxOpenPDB(sys.argv[1], False)
    
if __name__ == "__main__": main()
