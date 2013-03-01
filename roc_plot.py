#!/usr/bin/env python

from pylab import *
#from pprint import pprint
import sys

def main():
    filename = sys.argv[1]
    input = open(filename, 'r')
    
    result = []
    wt_score = 0.0
    for line in input:
        if line[0] == '#': continue
        data = line.split()
        #if len(data) ==  2:
        if 'WT' in line:
            wt_score = eval(data[1])
        elif len(data) > 2:
            diff = eval(data[1]) - wt_score
            label = data[2]
            result.append((diff, label))

    result.sort(key = lambda tup : tup[0], reverse = True)
    #pprint(result)

    T, F = 0, 0
    x, y = [0.0], [0.0]
    for (diff, label) in result:
        if label == 'T': T += 1
        else: F += 1
        x.append(F)
        y.append(T)

    x = [a / (F + 0.0) for a in x]
    y = [b / (T + 0.0) for b in y]
    
    old_x = 0.0
    area = 0.0
    for i in range(len(x)):
        width = x[i] - old_x
        area += width * y[i]
        old_x = x[i]
        old_y = y[i]
    print "Area under curve is: %.3f" % area

    plot(x, y, 'bo-', c = 'g', linewidth = 3.5)
    t = np.arange(0.0, 1.2, 0.2)
    plot(t, t, 'r--', linewidth = 2.0)
    xlabel("False Positive Rate")
    ylabel("True Positive Rate")
    ylim([0, 1.01])
    xlim([-0.01, 1.01])
    show()

main()
