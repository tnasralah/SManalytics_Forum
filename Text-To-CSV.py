from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models
import gensim
from pymongo import MongoClient
from HTMLParser import HTMLParser
import io
import shutil
import pprint
import sys
from bs4 import BeautifulSoup
import pprint
import util_fetch_mongo as fm
import pandas
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import csv
import re, itertools

import csv

with open('C:\TuDiabetes_Code - Final\TechTypes_Text_New\All_Tech_Claen.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('C:\TuDiabetes_Code - Final\TechTypes_Text_New\All_Tech_Claen.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Posts'))
        writer.writerows(lines)
#
# def csv_writer(data, path):
#     """
#     Write data to a CSV file path
#     """
#     with open(path, 'ab') as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         for line in data:
#             writer.writerow(line)
#     csv_file.close()
#
# f = open("C:\TuDiabetes_Code - Final\TechTypes_Text_New\Tech-All.txt", 'r')
# for line in f:
#     l = line.strip()
# csv_writer(l, "C:\TuDiabetes_Code - Final\TechTypes_Text_New\Tech-All.csv")