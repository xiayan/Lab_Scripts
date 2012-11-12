#usage: select the hit and type "showZinc".  It will show the zinc webpage and copy the ID on clippboard

from pymol import cmd
import os
import re

def parseObjName(objName):
    tokens = objName.split("_")
    fileName = "_".join(tokens[:-1]) + ".pdb"
    molRank = int(tokens[-1])
    return fileName, molRank

def writeHit(output, fileName, molRank, zincID):
    line = zincID + ": " + fileName + "\tRank: " + str(molRank) + "\n" 
    output.write(line)

def getAndWriteZincID(filename, rank):
    pdbInput = open(filename, 'r')
    counter = 0
    titleRegex = "^COMPND *ZINC[0-9][0-9]*_[0-9]*"
    zincID = ""

    for line in pdbInput:
        if (re.match(titleRegex, line) != None):
            counter += 1
        if counter == rank:
            zincID = extractZincID(line)
            break;

    outputName = "ZINC_" + zincID + ".pdb"
    output = open(outputName, 'w')
    output.write("COMPND ZINC" + " " + zincID + " from " + filename + 
            " " + "number " + str(rank) + '\n')
    for line in pdbInput:
        if (re.match(titleRegex, line) == None):
            output.write(line)
        else:
            break;

    return zincID, outputName

def extractZincID(line):
    regex = "COMPND *ZINC([0-9]*)_[0-9]"
    m = re.search(regex, line)
    return m.group(1)

def openZincWebpage(zincID):
    url = "http://zinc.docking.org/substance/" + zincID
    openCommand = "open -a Safari " + url
    os.system(openCommand)

def moveAndWriteMolecule(outputName, zincID, fileName, molRank):
    resultDir = "Hits"
    if not (resultDir in os.listdir(os.getcwd())) or not (os.path.isdir(resultDir)):
        os.system("mkdir " + resultDir)

    os.system("mv " + outputName + " " + resultDir)
    os.chdir(resultDir)
    writeHitFile(zincID, fileName, molRank)
    os.chdir("../")

def writeHitFile(zincID, fileName, molRank):
    outputFile = open("Hits.txt", "a")
    outputFile.write("ZINC: " + " " + zincID + " in " + fileName + 
            " number: " + str(molRank) + "\n")

def YXShowZINC():
    objName = cmd.identify("sele",1)[0][0]
    lastName = ""
    
    for objTuple in cmd.identify("sele", 1):
        objName = objTuple[0]
        if objName == lastName:
            continue
        lastName = objName
        fileName, molRank = parseObjName(objName)

        if fileName in os.listdir(os.getcwd()):
            zincID, outputName = getAndWriteZincID(fileName, molRank)
            openZincWebpage(zincID)
            moveAndWriteMolecule(outputName, zincID, fileName, molRank)
        else:
            print "Make sure to cd to the right directory"
    
cmd.extend("showZinc", YXShowZINC)
