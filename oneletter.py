#!/usr/bin/python

import string
import sys

def main():
    AA = dict([('GLY', 'G'), ('ALA', 'A'), ('SER', 'S'), ('THR', 'T'), ('CYS', 'C'), ('VAL', 'V'), \
	('LEU', 'L'), ('ILE', 'I'), ('MET', 'M'), ('PRO', 'P'), ('PHE', 'F'), ('TYR', 'Y'), ('TRP', 'W'), \
	('ASP', 'D'), ('GLU', 'E'), ('ASN', 'N'), ('GLN', 'Q'), ('HIS', 'H'), ('LYS', 'K'), ('ARG', 'R'), \
    ('ACYS', 'C')])

    codeList = []
    counter = 0
    pdb_index = 1
    chain = ""
    old_threeCode = ""

    assert(len(sys.argv) == 3)
    pdb = open(sys.argv[1], 'r')
    start, end = sys.argv[2].split("-")
    start, end = eval(start), eval(end)
	# pull out the first index and chain and first PDB residue number
    for line in pdb:
        element = line.split()
        if (len(element) > 3) and (element[0] == 'ATOM') and (element[3][-3:] in AA):
            chain = element[4]
            pdb_index = eval(element[5])
            old_threeCode = element[3][-3:]
            break

    # Generate one letter code
    index = pdb_index
    for line in pdb:
        element = line.split()
        if (len(element) > 3) and (element[0] == 'ATOM') and (element[3][-3:] in AA):
            number = eval(element[5])

            if number != index:
                index = number
                oneCode = AA[old_threeCode]
                print oneCode
                codeList.append(oneCode)
                old_threeCode = element[3][-3:]

        if (element[0] == 'END' or element[0] == 'TER') and (len(codeList) > 0):
            break

        if len(element) > 4 and element[4] != chain:
            break

    # Append the last residue
    oneCode = AA[old_threeCode]
    codeList.append(oneCode)

    pdb.close()
    print codeList
    singleLine = ''
    for i in range(start - pdb_index, end - pdb_index + 1):
        singleLine = singleLine + codeList[i]

    print singleLine
    #print 'Total' + ' ' + str(len(codeList)) + ' ' + 'residues'

main()
