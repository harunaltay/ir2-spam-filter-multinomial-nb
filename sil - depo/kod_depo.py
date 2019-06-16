from collections import defaultdict
import math
import glob
import os
import re

path = "dataset\\training\\spam"
DF = defaultdict(int)
for filename in glob.glob(os.path.join(path, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in set(words):
        if len(word) >= 3 and word.isalpha():
            DF[word] += 1

i = 0
for k, v in DF.items():
    i += 1
    print(i, k, v)

doccounter = 240
# Now you can compute IDF.
IDF = dict()
for word in DF:
    IDF[word] = math.log(doccounter / float(DF[word]))
    # Don't forget that python2 uses integer division.
