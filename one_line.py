"""print one line amino acid sequence"""
#!/usr/bin/python

import re
import sys
from ast import literal_eval

def main():
    """ print one line amino acid sequence """
    file_name = sys.argv[1]
    chain = sys.argv[2]
    if chain == None:
        chain = 'A'

    aa_map = dict([('GLY', 'G'), ('ALA', 'A'), ('SER', 'S'), ('THR', 'T'), \
            ('CYS', 'C'), ('VAL', 'V'), ('LEU', 'L'), ('ILE', 'I'), \
            ('MET', 'M'), ('PRO', 'P'), ('PHE', 'F'), ('TYR', 'Y'), \
            ('TRP', 'W'), ('ASP', 'D'), ('GLU', 'E'), ('ASN', 'N'), \
            ('GLN', 'Q'), ('HIS', 'H'), ('LYS', 'K'), ('ARG', 'R'), \
            ('ACYS', 'C')])

    regex = "^ATOM\s+[0-9]+\s+[A-Z0-9]+\s+[A-Z][A-Z][A-Z]\s+" \
            + chain +"\s+[0-9]+"

    in_file = open(file_name, 'r')
    start_num = -1
    one_line = []

    for line in in_file:
        if len(line.split()) < 5:
            continue
        if line.split()[4] != chain:
            continue
        if re.match(regex, line) != None:
            aa_name = line.split()[3]
            aa_num = literal_eval(line.split()[5])
            if aa_num != start_num:
                start_num = aa_num
                one_line.append(aa_name)

    result = []
    for aan in one_line:
        if aan in aa_map.keys():
            result.append(aa_map[aan])
        else:
            result.append('X')
    # print "".join([aa_map[a] for a in one_line])
    print "".join(result)

main()
