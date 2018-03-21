#!/usr/bin/python

import sys
import urllib
import gzip
import shutil

CONTENT_MIRROR="http://ftp.uk.debian.org/debian/dists/stable/main/"

#func for getting DL progress %, taken from : https://stackoverflow.com/questions/51212/how-to-write-a-download-progress-indicator-in-python
def dlProgress(count, blockSize, totalSize):
      percent = int(count*blockSize*100/totalSize)
      sys.stdout.write("%2d%%" % percent)
      sys.stdout.write("\b\b\b")



#check that script is getting the right # of args, if not print usage and exit
#will check validity of the arch when we try to pull the .gz
NUMARGS = len(sys.argv)
if not NUMARGS == 2:
    print("correct usage is: `python_stats.py ARCH` where arch is a valid arch i.e amd64 mips etc")


#get the architecture from command line arg
ARCH = str(sys.argv[1])

print("Attempting to pull the contents package of " + ARCH + " Using the mirror: " + CONTENT_MIRROR)
# $MIRROR_URL + "Contents-" + $ARCH + ".gz"
CONTENTS_GZ = CONTENT_MIRROR + "Contents-" + ARCH + ".gz"
urllib.urlretrieve (CONTENTS_GZ, "/tmp/contents.gz", reporthook=dlProgress)

#gunzip the file: taken from: https://stackoverflow.com/a/44712152
with gzip.open('/tmp/contents.gz', 'rb') as f_in:
    with open('/tmp/contents.txt', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

#neither the gunzip or the urlretreive complain if the file already exists, so just going to be okay with it overwriting existing files.

#begin parsing test file:
# remove column1, from the file and put into a separate file: /tmp/contents_column2.txt
# slightly modified logic from: https://stackoverflow.com/a/10158699
f = open("/tmp/contents.txt", "r")
g = open("/tmp/contents_column2.txt", "w")

for line in f:
    if line.strip():
        g.write("\t".join(line.split()[-1:]) + "\n")

f.close()
g.close()
