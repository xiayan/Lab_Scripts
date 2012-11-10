#! /usr/bin/python
from sys import argv
from os import system, chdir, listdir, path, getcwd

def filename(url):
    return url.split("/")[-1]

def detect_duplicate(name):
    cwd = getcwd()
    return name in listdir(cwd)


def main():
    assert(len(argv) == 2)
    url = argv[1]
    outputname = filename(url)
    home = path.expanduser("~")
    dest = home+"/Dropbox/Wall_Pictures/"
    chdir(dest)
    if detect_duplicate(outputname):
        print "File already existed"
    else:
        the_command = 'curl '+url+' > '+outputname
        print the_command
        system(the_command)
    print "Done!"
    system('open '+dest + ' -a Finder')

main()