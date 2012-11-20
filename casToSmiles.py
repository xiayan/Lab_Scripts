import urllib
import os,sys

def casToSmiles(casID):
    try:
        f = urllib.urlopen("http://zinc.docking.org/cas/" + casID)
    except:
        print "No " + casID + " found in ZINC"
        return ""
    start = False
    zincPage = ""
    zincID = ""
    smileString = ""

    for line in f:
        if "substance-list" in line:
            start = True
        if ("href" in line) and start:
            startIndex = line.find("\"")
            endIndex = line.find("\"", startIndex + 1)
            zincPage = line[startIndex + 1 : endIndex]
            start = False
            break;

    f.close()
    
    try:
        f = urllib.urlopen(zincPage)
    except:
        print "No " + casID + " found in ZINC"
        return ""

    for line in f:
        if 'id="item-smiles"' in line:
            valueIndex = line.find("value")
            startIndex = line.find("\"", valueIndex + 1)
            endIndex = line.find("\"", startIndex + 1)
            smileString = line[startIndex + 1 : endIndex]

    f.close()
    
    print zincPage
    print smileString

    idStart = zincPage.rfind("/")
    zincID = "ZINC" + zincPage[idStart + 1 :]

    return smileString + "\t\t" + zincID

def main():
    fileInput = os.path.isfile(sys.argv[1])
    output = open("output.smi", "w")

    if fileInput:
        f = open(sys.argv[1], "r")
        for line in f:
            result = casToSmiles(line)
            output.write(result + "\n")
            print result
    else:
        result = casToSmiles(sys.argv[1])
        output.write(result);
        print result 

main()
