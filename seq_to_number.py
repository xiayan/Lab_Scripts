#!/usr/bin/python
import sys

def main():

    AA = dict([('G', "1"), ('A', "2"), ('S', "3"), ('T', "4"), ('C', "5"), ('V', "6"), \
        ('L', "7"), ('I', "8"), ('M', "9"), ('P', "10"), ('F', "11"), ('Y', "12"), ('W', "13"), \
        ('D', "14"), ('E', "15"), ('N', "16"), ('Q', "17"), ('H', "18"), ('K', "19"), ('R',"20"), ('-', "21"), ('\n', '\n')])

    if sys.argv[1] == "":
        input_name = "native.txt"
    else:
        input_name = sys.argv[1]
    output_name = input_name.split(".")[0] + "_tran.txt"
    inputFile = open(input_name, 'r')
    outputFile = open(output_name, 'w')

    for line in inputFile:
        output = " ".join(AA[letter] for letter in line)
        outputFile.write(output)

    inputFile.close()
    outputFile.close()

main()