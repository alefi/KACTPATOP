#!/usr/bin/python3
# coding=utf_8

"""
This program shrinks all file names length into working --dir
to 225-bytes maximum UTF-8 encoded, if applicable.
If no option --commit present, it only display files
which contains all exceeded 255-bytes length file names.
You can locate these files and rename it by hands.
"""

import argparse, os, sys
from collections import defaultdict

def utf8len(s):
    """Counts UTF-8 encoded string's length."""
    return len(s.encode(encoding='utf_8'))

def fineCut(s, targetSLength):
    """Cuts string to desired length."""
    s = s[:-1]
    if (utf8len(s) >= targetSLength):
        s = fineCut(s, targetSLength)
    return s

def fileRead(mydir, commit):
    """Reads files recursively and renames it if need."""
    data = defaultdict(list)
    try:
        for fName in os.listdir(mydir):
            pathSrc = os.path.join(mydir, fName)
            if os.path.isfile(pathSrc):
                """Shrinks only files over 255-bytes length currenty."""
                if (utf8len(fName) > 255):
                    if '.' in fName:
                        pieces = fName.split('.')
                        fExt = "."+ pieces[len(pieces)-1]
                        newfName = " ".join(pieces[:-1])
                    else:
                        newfName = fName
                        fExt = ''
                    newfName = fineCut(newfName, 255-utf8len(fExt)) + fExt
                    pathDst = os.path.join(mydir, newfName)
                    data[mydir].append(fName)
                    if commit:
                        os.replace(pathSrc, pathDst)
            else:
                for k, v in fileRead(pathSrc, commit).items():
                    data[k].append(str(v).strip("'[]'"))
    except OSError as e:
        print(e, file=sys.stderr)
    return data

def printModList(ml):
    """Prints dictionary in human friendly format."""
    count = 0
    for k in ml:
        print (k)
        for v in ml[k]:
            print(v)
            count += 1
    return count

"""Read CL arguments"""
parser = argparse.ArgumentParser(add_help=True, description="Shrinks all file names length into working --dir to 225-bytes maximum UTF-8 encoded, if applicable. If no option --commit present, it only dysplay files which contains all exceeded 255-bytes length file names. You can locate these files and rename it by hands.")
parser.add_argument("dir", type = str, help = "Working directory (Where to find files to shrink)")
parser.add_argument("-c", "--commit", help = "Commit changes (Actually rename matched files!)", action = "store_true")
args = parser.parse_args()

""""main"""
mydir = args.dir
if os.path.exists(mydir):
    modfList = fileRead(mydir, args.commit)
    if (args.commit) & (len(modfList) > 0):
        count = printModList(modfList)
        print('В папке %s переименовано %i файлов.' %(mydir, count))
    elif len(modfList) > 0:
        count = printModList(modfList)
        print('В папке %s найдено %i файлов.' %(mydir, count))
    else:
            print('В папке %s длинных имен файлов не найдено.' %mydir)
else:
    print('Не верно указан путь: %s' %args.dir)
