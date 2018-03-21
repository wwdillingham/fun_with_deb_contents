#!/usr/bin/python

import sys
import urllib

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
