#!/usr/bin/python
from sys import argv

def main():
    inputFile = open(argv[1], 'r')
    zinc = argv[2]
    outFile = open(argv[2]+'.pdb', 'w')
    write_flag = False
    for line in inputFile:
        if "COMPND" in line and zinc in line:
            write_flag = True
        if write_flag:
            outFile.write(line)
        if "END" in line and write_flag:
            break

    outFile.close()
    print "Done"

main()
