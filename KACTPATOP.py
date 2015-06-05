import os, sys
from collections import defaultdict

mydir = "/home/alexey/test-255"

def utf8len(s):
    """Counts UTF-8 encoded string's length."""
    return len(s.encode(encoding='utf_8'))

def fineCut(s, targetSLength):
    """Cuts string to desired length."""
    s = s[:-1]
    if (utf8len(s) >= targetSLength):
        s = fineCut(s, targetSLength)
    return s

def fileRead(mydir, count):
    """Reads files recursively and renames it if need."""
    try:
        for fName in os.listdir(mydir):
            pathSrc = os.path.join(mydir, fName)
            if os.path.isdir(pathSrc):
                count = fileRead(pathSrc, count)
            else:
                #Shrinks only files with 255+ length currenty.
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
                    os.replace(pathSrc, pathDst)
                    count += 1
    except OSError as e:
        print(e, file=sys.stderr)
    return count    

#main
if os.path.exists(mydir):
    count = fileRead(mydir, 0)
    if count > 0:
        print('В папке %s переименовано %i файлов.' %(mydir, count))
    else:
        print('В папке %s длинных имен файлов не найдено.' %mydir)
else:
    print('Не верно указан путь.')