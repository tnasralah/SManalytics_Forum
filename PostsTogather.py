import sys
import pandas as pd
import numpy as np
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
import LDA as lda


df = pd.read_csv('C:\TuDiabetes_Code - Final\TechTypes_Text_New\Discussions_Tech.csv')
assert isinstance(df, pd.DataFrame) # for pycharm code completion
TARGET_D_LIST= df['TARGET_D'].tolist()
df_TargetD= df['TARGET_D']
df = df.drop('TARGET_D', 1)
print '================================== kddcup98.csv Data =================================='
print df.head(3)
print '================================== Data describtion=================================='
print df.describe()
