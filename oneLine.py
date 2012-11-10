#!/usr/bin/python

import re
import sys

def main():
    fileName = sys.argv[1]
    chain = sys.argv[2]
    if chain == None:
        chain = 'A'

    AA = dict([('GLY', 'G'), ('ALA', 'A'), ('SER', 'S'), ('THR', 'T'), ('CYS', 'C'), ('VAL', 'V'), \
    ('LEU', 'L'), ('ILE', 'I'), ('MET', 'M'), ('PRO', 'P'), ('PHE', 'F'), ('TYR', 'Y'), ('TRP', 'W'), \
    ('ASP', 'D'), ('GLU', 'E'), ('ASN', 'N'), ('GLN', 'Q'), ('HIS', 'H'), ('LYS', 'K'), ('ARG', 'R'), \
    ('ACYS', 'C')])

    regex = "^ATOM\s+[0-9]+\s+[A-Z0-9]+\s+[A-Z][A-Z][A-Z]\s+" + \
    chain +"\s+[0-9]+"

    inFile = open(fileName, 'r');
    startNum = -1
    oneLine = []

    for line in inFile:
        if line.split()[4] != chain:
            continue;
        if (re.match(regex, line) != None):
            aaName = line.split()[3]
            aaNumber = eval(line.split()[5])
            if aaNumber != startNum:
                startNum = aaNumber
                oneLine.append(aaName)

    print "".join([AA[a] for a in oneLine])

main()
