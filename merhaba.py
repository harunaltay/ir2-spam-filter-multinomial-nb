from collections import defaultdict
import math
import glob
import os
import re

i = 0

path_training_spam = "dataset\\training\\spam"
path_training_leg = "dataset\\training\\legitimate"
path_test_spam = "dataset\\test\\spam"
path_test_leg = "dataset\\test\\legitimate"

DF_train_spam = defaultdict(int)
WordsTotal_train_spam = defaultdict(int)

DF_train_leg = defaultdict(int)
WordsTotal_train_leg = defaultdict(int)

for filename in glob.glob(os.path.join(path_training_spam, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            WordsTotal_train_spam[word] += 1  # defaultdict simplifies your "if key in word_idf: ..." part.

    for word in set(words):
        if word == 'subject':
            continue
        if word.isalpha():
            DF_train_spam[word] += 1  # defaultdict simplifies your "if key in word_idf: ..." part.


for filename in glob.glob(os.path.join(path_training_leg, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            WordsTotal_train_leg[word] += 1  # defaultdict simplifies your "if key in word_idf: ..." part.

    for word in set(words):
        if word == 'subject':
            continue
        if word.isalpha():
            DF_train_leg[word] += 1  # defaultdict simplifies your "if key in word_idf: ..." part.


for key, value in sorted(WordsTotal_train_spam.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    if len(key) == 1:
        continue
    i += 1
    print(i, key, value)
    if i >= 200:
        break

WordsTotal_test_spam = defaultdict(int)
WordsTotal_test_leg = defaultdict(int)

for filename in glob.glob(os.path.join(path_test_spam, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            WordsTotal_test_spam[word] += 1  # defaultdict simplifies your "if key in word_idf: ..." part.



for filename in glob.glob(os.path.join(path_test_leg, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())



# for key, value in sorted(DF.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
#     if len(key) == 1:
#         continue
#     i+=1
#     print(i, key, value)
#     if i>=200:
#         break

# doccounter = 240
# # Now you can compute IDF.
# IDF = dict()
# for word in DF:
#     IDF[word] = math.log(doccounter / float(DF[word]))
#     # Don't forget that python2 uses integer division.
