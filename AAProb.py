#calculate aa propensity
#takes two arguments: pdb name and amino acid name

from rosetta import *
import sys

def main():
    rosetta.init() 
    fileName = sys.argv[1] 
    pose = Pose(fileName) 
    totalNum = pose.total_residue() 
    
    aaCounts = dict() 
    
    for i in range(1,totalNum+1):
        aaName = pose.residue(i).name()[0:3] 
        if aaCounts.has_key(aaName):
            aaCounts[aaName][0] = aaCounts[aaName][0] + 1 
        else:
            #build a key value pair, where the key is the three-letter aa name, value is a list of number
            aaCounts[aaName] = [1.0, 0.0, 0.0 ,0.0] 
            
        phiAngle = pose.phi(i) 
        psiAngle = pose.psi(i) 
            
        if (phiAngle >= -180 and phiAngle <= -45) and (psiAngle >= 90 and psiAngle <= 180):
            aaCounts[aaName][1] = aaCounts[aaName][1] + 1 
        elif (phiAngle >= -135 and phiAngle <= -45) and (psiAngle >= -80 and psiAngle <= 40):
            aaCounts[aaName][2] = aaCounts[aaName][2] + 1 
        else:
            aaCounts[aaName][3] = aaCounts[aaName][3] + 1 
            
    # if no second argument, print everything, else print specified aa.
    if len(sys.argv) < 3:
        for k, v in aaCounts.iteritems():
            print k, v 
            print "Pa = ", float(v[2] / v[0]) 
            print "Pb = ", float(v[1] / v[0]) 
            print "Pl = ", float(v[3] / v[0]) 
    else:
        aaChoice = sys.argv[2].upper() 
        aaChoice = aaChoice[0:3] 
        if aaCounts.has_key(aaChoice):
            print aaChoice, aaCounts[aaChoice] 
            print "Pa = ", float(aaCounts[aaChoice][2] / aaCounts[aaChoice][0]) 
            print "Pb = ", float(aaCounts[aaChoice][1] / aaCounts[aaChoice][0]) 
            print "Pl = ", float(aaCounts[aaChoice][3] / aaCounts[aaChoice][0]) 
        else:
            print "No AA: ", aaChoice 
            
if __name__ == "__main__": main() 
