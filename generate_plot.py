#!/usr/bin/python2.5

import os,sys
from rmsd import yx_ca_rmsd

def main():
    start = 9
    end = 24
    filename = "rmsd.txt"

    wtname = sys.argv[1]
    cwd = os.getcwd()

    fileList = [pdb for pdb in os.listdir(cwd) if pdb != wtname if "2ANO" in pdb]

    for_octave = open(filename, "w")
    for result in fileList:
        current_rmsd = yx_ca_rmsd(wtname, result, start, end)
        for_octave.write(str(current_rmsd) + '\n')

main()