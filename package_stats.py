#!/usr/bin/python

import sys
import urllib
import gzip
import shutil
import operator

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

#convert commas to new lines, and put the contents into a separate file (/tmp/separated_list)
with open('/tmp/contents_column2.txt') as infile:
    contents = infile.read()
    contents = contents.replace(',', '\n')
    f = open( '/tmp/separated_list', 'w' )
    f.write(contents)
    f.close()

#now we have commas removed, each item is on its own line.
#need to harness the last item in the optional/optional/package structure and make it just be "package"
f = open("/tmp/separated_list", "r")
g = open("/tmp/packages_only", "w")

for line in f:
    g.write(line.split('/', -1)[-1])

#results = sorted(results, reverse=True)[:10]
#print(results)
frequency = {}
package_list = open('/tmp/packages_only', 'r')
for package in package_list:
    count = frequency.get(package,0)
    frequency[package] = count + 1

frequency_list = frequency.keys()

# we now have a dict, frequency and need to sort by value, decsdencing, and print out top ten

#get the maximal value, and print out the key, then the value, then remove that maximal entry from the dict, do this ten times to get top 10
for i in range(10):
    maximal = max(frequency.iteritems(), key=operator.itemgetter(1))[0]
    print(maximal.strip('\n')), frequency[maximal]
    del frequency[maximal]

