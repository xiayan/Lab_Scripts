#!/usr/bin/python2.5

import rosetta
import sys, os.path, math
from structural_alignment import kabsch_alignment
import getopt

total_square = 0.0

def calculateRMS(pose1, pose2, i, rmsdList):
    v1 = pose1.residue(i).xyz("CA")
    v2 = pose2.residue(i).xyz("CA")
    square = (v1.x - v2.x)**2 + (v1.y - v2.y)**2 + (v1.z - v2.z)**2
    root = math.sqrt(square)
    rmsdList[i - 1] = rmsdList[i - 1] + root

    global total_square
    total_square = total_square + square

def relax_filename(filename, index):
    if index < 10:
        relax_filename = filename + "_000" + str(index) + ".pdb"
    elif index >= 10 and index < 100:
        relax_filename = filename + "_00" + str(index) + ".pdb"
    elif index >= 100 and index < 1000:
        relax_filename = filename + "_0" + str(index) + ".pdb"
    else:
        relax_filename = filename + "_" + str(index) + ".pdb"
    return relax_filename

def outputMinMax(totalRMSD, compareName):
    minRMSD = min(totalRMSD)
    maxRMSD = max(totalRMSD)
    minIndex = totalRMSD.index(minRMSD) + 1
    maxIndex = totalRMSD.index(maxRMSD) + 1
    minName = relax_filename(compareName, minIndex)
    maxName = relax_filename(compareName, maxIndex)
    print "min RMSD: ", str(minRMSD), " ", minName
    print "max RMSD: ", str(maxRMSD), " ", maxName

def main():
    opts, args = getopt.getopt(sys.argv[3:], 'i')
    show_index = 0

    for o in opts:
        if '-i' in o:
            show_index = 1

    rosetta.init()
    file_index = 1
    wtName = sys.argv[1]
    compareName = sys.argv[2]
    relax_name = relax_filename(compareName, file_index)

    outputName = wtName.split('.')[0] + '_vs_' + compareName + ".txt"
    output = open(outputName, 'w')

    pose1 = rosetta.Pose(wtName)
    total_residue = pose1.total_residue()
    rmsdList = [0.00] * total_residue
    totalRMSD = []

    while os.path.isfile(relax_name):
        pose2 = rosetta.Pose(relax_name)

        if pose1.total_residue() != pose2.total_residue():
            print "Residue number not equal"
            break
        else:
            kabsch_alignment(pose1, pose2, range(1, total_residue + 1), range(1, total_residue + 1))
            for i in range(1, total_residue + 1):
                calculateRMS(pose1, pose2, i, rmsdList)

        ro_rmsd = rosetta.CA_rmsd(pose1, pose2)
        totalRMSD.append(ro_rmsd)
        print "rosetta generated rmsd: " + str(ro_rmsd)

        global total_square
        me_rmsd = math.sqrt(total_square / total_residue)
        print "me generated rmsd: " + str(me_rmsd)
        total_square = 0.0

        file_index = file_index + 1
        relax_name = relax_filename(compareName, file_index)

    if file_index == 1:
        print "No relaxation file"
    else:
        file_index = file_index - 1
        rmsd_total = 0.0

        if file_index > 0:
            for rmsd in totalRMSD:
                rmsd_total = rmsd_total + rmsd
            averageRMSD = rmsd_total / file_index
            print "average rmsd: ", str(averageRMSD)
            outputMinMax(totalRMSD, compareName)

            print "outputing " + outputName + "..."
            for index in range(1, total_residue + 1):
                rmsdList[index - 1] = rmsdList[index - 1] / file_index
                if show_index:
                    output.write(str(index) + '\t' + str(rmsdList[index - 1]) + '\n')
                else:
                    output.write(str(rmsdList[index - 1]) + '\n')
            output.write(outputName.split('.')[0] + "_relax\taverage rmsd: " + str(averageRMSD))

    output.close()
    print "Done"

main()