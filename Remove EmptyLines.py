from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import fileinput
from gensim import corpora, models
import gensim
from pymongo import MongoClient
from HTMLParser import HTMLParser
import io
import shutil
import pprint

C= 0
def removeEmptyLines(line):
    if len(line.strip()) >= 1 :
        print line
        with open('C:\TuDiabetes_Code - Final\TechTypes_Text_New\Physical_Activity_Clean_Lines.txt', 'a') as the_file:
            the_file.write(line)
#==============================================================

f = open("C:\TuDiabetes_Code - Final\TechTypes_Text_New\Physical_Activity_Clean.txt", 'r')
count=0
for line in f:
    if len(line.strip())>=1: C=C+1
    removeEmptyLines(line)
    count += 1
print "count = " + str(count) +"      C = "+ str(C)


# print number of lines
from textblob import TextBlob
txt = """Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned with the inter
actions between computers and human (natural) languages."""
blob = TextBlob(txt)
print(blob.noun_phrases)