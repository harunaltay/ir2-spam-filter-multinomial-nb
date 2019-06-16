# CSE586 IR - HW 2 - Spam Filter Multinomial Naive Bayes
# Harun Altay
# Note: please note that variable and other names are long and self-informative

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

# TRAIN ----------------------------------------------------------------------------------

DF_train_spam = defaultdict(int) # document frequency for spam
WordsTotal_train_spam = defaultdict(int) # whole words for spam

DF_train_leg = defaultdict(int) # document frequency for legitimates
WordsTotal_train_leg = defaultdict(int) # whole words for spam

# process the spam training folder
for filename in glob.glob(os.path.join(path_training_spam, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            WordsTotal_train_spam[word] += 1

    for word in set(words):
        if word == 'subject':
            continue
        if word.isalpha():
            DF_train_spam[word] += 1

# process the legitimate training folder
for filename in glob.glob(os.path.join(path_training_leg, '*.txt')):
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            WordsTotal_train_leg[word] += 1

    for word in set(words):
        if word == 'subject':
            continue
        if word.isalpha():
            DF_train_leg[word] += 1

top200words_train_spam = {}
top200words_train_leg = {}

i = 0
# populate top 200 spam words
for key, value in sorted(WordsTotal_train_spam.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    if len(key) < 3:
        continue
    i += 1
    top200words_train_spam[key] = value
    # print("{0:3} {1:13} # of occurance:{2:4}, Doc Frequency:{3:3}".format(i, key, value, DF_train_spam[key]))
    if i >= 200:
        break

# for k, v in top200words_train_spam.items():
#     print(k, v)


i = 0
# populate top 200 legitimate words
for key, value in sorted(WordsTotal_train_leg.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
    if len(key) < 3:
        continue
    i += 1
    top200words_train_leg[key] = value
    # print("{0:3} {1:13} # of occurance:{2:4}, Doc Frequency:{3:3}".format(i, key, value, DF_train_leg[key]))
    if i >= 200:
        break

# for k, v in top200words_train_leg.items():
#     print(k, v)

dictionary_size_spam = 0
dictionary_size_leg = 0

for k, v in top200words_train_spam.items():
    dictionary_size_spam += v

for k, v in top200words_train_leg.items():
    dictionary_size_leg += v

print("dictionary_size_spam", dictionary_size_spam)
print("dictionary_size_leg", dictionary_size_leg)

vocabulary_size = 350

number_of_spams_without_smooting = 0
number_of_spams_with_smooting = 0

number_of_legs_without_smooting = 0
number_of_legs_with_smooting = 0

# TEST - SPAM -----------------------------------------------------------------------------------------

# process the test/spam folder

i = 0
for filename in glob.glob(os.path.join(path_test_spam, '*.txt')):
    words_dict = defaultdict(int)
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            words_dict[word] += 1

    total_spam_without_smooting = 0.0
    total_leg_without_smooting = 0.0

    total_spam_with_smooting = 0.0
    total_leg_with_smooting = 0.0

    keys_spam = top200words_train_spam.keys()
    keys_leg = top200words_train_leg.keys()

    for k, v in words_dict.items():
        if k in keys_spam:
            total_spam_without_smooting += (top200words_train_spam[k] / dictionary_size_spam) ** v
            total_spam_with_smooting += ((top200words_train_spam[k] + 1) / (
                    dictionary_size_spam + vocabulary_size)) ** v
        else:
            total_spam_with_smooting += ((0 + 1) / (dictionary_size_spam + vocabulary_size)) ** v

    for k, v in words_dict.items():
        if k in keys_leg:
            total_leg_without_smooting += (top200words_train_leg[k] / dictionary_size_leg) ** v
            total_leg_with_smooting += ((top200words_train_leg[k] + 1) / (
                    dictionary_size_leg + vocabulary_size)) ** v
        else:
            total_leg_with_smooting += ((0 + 1) / (dictionary_size_leg + vocabulary_size)) ** v

    class_without_smoothing = ""
    class_with_smoothing = ""

    if total_spam_without_smooting > total_leg_without_smooting:
        class_without_smoothing = "spam"
        number_of_spams_without_smooting += 1
    else:
        class_without_smoothing = "legitimate"

    if total_spam_with_smooting > total_leg_with_smooting:
        class_with_smoothing = "spam"
        number_of_spams_with_smooting += 1
    else:
        class_with_smoothing = "legitimate"

    i += 1
    print(i, filename)
    print("Without Smoothing - spam: {0}, legitimate: {1}, class: {2}".format(total_spam_without_smooting,
                                                                              total_leg_without_smooting,
                                                                              class_without_smoothing))
    print("With Smoothing    - spam: {0}, legitimate: {1}, class: {2}".format(total_spam_with_smooting,
                                                                              total_leg_with_smooting,
                                                                              class_with_smoothing))
    print()


print()
print("number_of_spams_without_smooting", number_of_spams_without_smooting, ", %",
      number_of_spams_without_smooting * 100 / 240)
print("number_of_spams_with_smooting", number_of_spams_with_smooting, ", %",
      number_of_spams_with_smooting * 100 / 240)

print()
print("*********************************************************************************************")
print("*********************************************************************************************")
print("*********************************************************************************************")
print()

number_of_spams_without_smooting = 0
number_of_spams_with_smooting = 0

number_of_legs_without_smooting = 0
number_of_legs_with_smooting = 0

# TEST - LEGITIMATE -----------------------------------------------------------------------------------------

# process the test/legitimate folder

i = 0
for filename in glob.glob(os.path.join(path_test_leg, '*.txt')):
    words_dict = defaultdict(int)
    words = re.findall(r'\w+', open(filename).read().lower())
    for word in words:
        if word == 'subject':
            continue
        if word.isalpha():
            words_dict[word] += 1

    total_spam_without_smooting = 0.0
    total_leg_without_smooting = 0.0

    total_spam_with_smooting = 0.0
    total_leg_with_smooting = 0.0

    keys_spam = top200words_train_spam.keys()
    keys_leg = top200words_train_leg.keys()

    for k, v in words_dict.items():
        if k in keys_spam:
            total_spam_without_smooting += (top200words_train_spam[k] / dictionary_size_spam) ** v
            total_spam_with_smooting += ((top200words_train_spam[k] + 1) / (
                    dictionary_size_spam + vocabulary_size)) ** v
        else:
            total_spam_with_smooting += ((0 + 1) / (dictionary_size_spam + vocabulary_size)) ** v

    for k, v in words_dict.items():
        if k in keys_leg:
            total_leg_without_smooting += (top200words_train_leg[k] / dictionary_size_leg) ** v
            total_leg_with_smooting += ((top200words_train_leg[k] + 1) / (
                    dictionary_size_leg + vocabulary_size)) ** v
        else:
            total_leg_with_smooting += ((0 + 1) / (dictionary_size_leg + vocabulary_size)) ** v

    class_without_smoothing = ""
    class_with_smoothing = ""

    if total_spam_without_smooting > total_leg_without_smooting:
        class_without_smoothing = "spam"
        number_of_spams_without_smooting += 1
    else:
        class_without_smoothing = "legitimate"

    if total_spam_with_smooting > total_leg_with_smooting:
        class_with_smoothing = "spam"
        number_of_spams_with_smooting += 1
    else:
        class_with_smoothing = "legitimate"

    i += 1
    print(i, filename)
    print("Without Smoothing - spam: {0}, legitimate: {1}, class: {2}".format(total_spam_without_smooting,
                                                                              total_leg_without_smooting,
                                                                              class_without_smoothing))
    print("With Smoothing    - spam: {0}, legitimate: {1}, class: {2}".format(total_spam_with_smooting,
                                                                              total_leg_with_smooting,
                                                                              class_with_smoothing))
    print()


number_of_legs_without_smooting = 240 - number_of_spams_without_smooting
number_of_legs_with_smooting = 240 - number_of_spams_with_smooting

print()
print("number_of_legs_without_smooting", number_of_legs_without_smooting, ", %",
      number_of_legs_without_smooting * 100 / 240)
print("number_of_legs_with_smooting", number_of_legs_with_smooting, ", %",
      number_of_legs_with_smooting * 100 / 240)
