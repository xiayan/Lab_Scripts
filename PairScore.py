from rosetta import *
import os
import sys
import CleanPDB

def main():
    assert( len(sys.argv)>3 )
    
    #first argument: pdb filename second and third argument: resNum and chain ID
    pdbFile = sys.argv[1]
    rsd1 = int(sys.argv[2][:-1])
    rsd2 = int(sys.argv[3][:-1])
    chain1 = sys.argv[2][-1].upper()
    chain2 = sys.argv[3][-1].upper()
    
    global PDB # file handeler for input pdb file
    
    try:
        PDB = open(pdbFile, 'r')
    except IOError:
        print "Cannot open file"
        sys.exit()
    
    # generate clean version of input file 
    tempPDB = open('.temp.pdb', 'w+b')
    CleanPDB.clean(PDB, tempPDB)
            
    # Rosetta calculation
    try:
        rosetta.init()
        pose = Pose(".temp.pdb")
    
        scorefxn = create_score_function("standard")
        poseResNum1 = pose.pdb_info().pdb2pose(chain1, rsd1)
        poseResNum2 = pose.pdb_info().pdb2pose(chain2, rsd2)
    
        emap = TwoBodyEMapVector()
        scorefxn.eval_ci_2b(pose.residue(poseResNum1), pose.residue(poseResNum2), pose, emap)
        print "\n\nInteractions between ", pose.residue(poseResNum1).name() + str(rsd1) + chain1,  " and ", \
        pose.residue(poseResNum2).name() + str(rsd2) + chain2, ":"
        print "Attraction: ", emap[fa_atr]
        print "Repulsion: ", emap[fa_rep]
        print "Solvation: ", emap[fa_sol]
        print "Sidechain-backbone hydrogen bond: ", emap[hbond_bb_sc]
        print "Sidechain-sidechain hydrogen bond: ", emap[hbond_sc]
        print ""
    except:
        print sys.exc_info()
        
    PDB.close()
    tempPDB.close()
    os.remove(".temp.pdb")
        
if __name__ == "__main__": main() 