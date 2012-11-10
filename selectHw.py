#!/usr/bin/python

from random import sample
import sys

def main():
    numberOfQuestions = eval(sys.argv[1])
    homeworkNumber = eval(sys.argv[2])
    if homeworkNumber == None:
        homeworkNumber = 7

    print sorted(sample(range(1,numberOfQuestions + 1), homeworkNumber));

main()