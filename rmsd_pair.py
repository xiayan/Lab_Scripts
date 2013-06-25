#!/usr/bin/python2.5

import rosetta
import sys, os.path, math
from structural_alignment import kabsch_alignment
import getopt

total_square = 0.0

def calculateRMS(pose1, pose2, i, output, index):
    v1 = pose1.residue(i).xyz("CA")
    v2 = pose2.residue(i).xyz("CA")
    square = (v1.x - v2.x)**2 + (v1.y - v2.y)**2 + (v1.z - v2.z)**2
    global total_square
    total_square = total_square + square
    root = math.sqrt(square)
    if index:
        output.write(str(i) + '\t' + str(root) + '\n')
    else:
        output.write(str(root) + '\n')

def main():
    opts, args = getopt.getopt(sys.argv[3:], 'i')
    show_index = 0

    for o in opts:
        if '-i' in o:
            show_index = 1

    rosetta.init()
    wtName = sys.argv[1]
    compareName = sys.argv[2]

    outputName = wtName.split('.')[0] + '_vs_' + compareName.split('.')[0] + ".txt"

    pose1 = rosetta.Pose(wtName)
    pose2 = rosetta.Pose(compareName)

    use_me = True
    if pose1.total_residue() != pose2.total_residue():
        print "Residue number not equal", pose1.total_residue(), \
                                        pose2.total_residue()
        use_me = False
    else:
        output = open(outputName, 'w')
        total_residue = pose1.total_residue()

        kabsch_alignment(pose1, pose2, range(1, total_residue + 1), range(1, total_residue + 1))
        # RMSD calculated by my own function
        for i in range(1, total_residue + 1):
            calculateRMS(pose1, pose2, i, output, show_index)

    # RMSD calculated by PyRosetta
    ro_rmsd = rosetta.CA_rmsd(pose1, pose2)
    print "rosetta generated rmsd: " + str(ro_rmsd)

    if use_me:
        global total_square
        me_rmsd = math.sqrt(total_square / total_residue)
        print "me generated rmsd: " + str(me_rmsd)
        output.write(outputName.split('.')[0] + ":\t" + str(ro_rmsd))
        output.close()

    print "Done"

main()
