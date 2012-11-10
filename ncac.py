#Calculates N-CAlpha-C degree
#take 2 argument: pdb file name and residue number

from rosetta import *
import math
import sys

def main():
    rosetta.init();
    fileName = sys.argv[1];
    #pose = Pose("3ihw.clean.pdb");
    pose = Pose(fileName); 
    resNum = eval(sys.argv[2]);
    resNum = int(resNum);
    N_xyz = pose.residue(resNum).xyz("N");
    CA_xyz = pose.residue(resNum).xyz("CA");
    C_xyz = pose.residue(resNum).xyz("C");
    
    N_CA_vector = CA_xyz - N_xyz;
    CA_C_vector = CA_xyz - C_xyz;
    
    cosineAngle = N_CA_vector.dot(CA_C_vector) / (N_CA_vector.norm * CA_C_vector.norm);
    print "degree: ", math.acos(cosineAngle) * 180.0 / math.pi;
    
if __name__ == "__main__": main();
