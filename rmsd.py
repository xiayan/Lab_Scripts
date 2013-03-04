#!/usr/bin/python2.5

import rosetta, sys
from structural_alignment import kabsch_alignment

def yx_ca_rmsd(wt, comp, start=-1, end=-1):
    rosetta.init()
    pose1 = rosetta.Pose(wt)
    pose2 = rosetta.Pose(comp)
    if pose1.total_residue() != pose2.total_residue():
        print "Residue numbers are not the same"
        return
    else:
        total_residue = pose1.total_residue()
        kabsch_alignment(pose1, pose2, range(1, total_residue + 1), range(1, total_residue + 1))

        if start < 0 or end < 0 or end < start:
            start = 1
            end = total_residue

        ro_rmsd = rosetta.CA_rmsd(pose1, pose2, range(19))

        return ro_rmsd

def main():

    wtName = sys.argv[1]
    compareName = sys.argv[2]
    rmsd = yx_ca_rmsd(wtName, compareName)
    print rmsd

if __name__ == "__main__": main()

