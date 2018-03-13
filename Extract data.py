import sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import pprint
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import csv
import re, itertools

df = pd.read_csv('C:\TuDiabetes_Code - Final\discussions_Tech_Catigories.csv')
df=df[['cooked','topic_id','user_id']]

topic_set= set(df['topic_id'])
user_ids=list(df['user_id'])

len(topic_set)

Col=[]
Top_id=[]
c=0
for i in topic_set:
    dfnew= df[(df['topic_id']==i)]
    li=list(dfnew['cooked'])
    line= ". ".join(str(x) for x in li)
    Col.append(line)
    Top_id.append(i)
    c=i+1
#     print (line)
#     print ('\n\n')
#     with open('C:\TuDiabetes_Code - Final\TechDataCSV\discussions - ALL-Technology SubCatigories.txt', 'a') as the_file:
#         the_file.write(line+"\n")
    


# In[21]:

len(Col)


# In[22]:

dfli = pd.DataFrame(Col)
dfli['Topic_Disc']=dfli[0]
#dfli['Topic_Disc']= Col
dfli=dfli[['Topic_Disc']]


# In[23]:

print dfli.head(4)


# In[24]:

dfli.to_csv('C:\TuDiabetes_Code - Final\TechDataCSV\RowTopicDiscCsv\discussions - ALL-Technology - ALL-Technology SubCatigories.csv', sep=',')


# In[25]:

print c


# In[26]:

i=0
for i in range(1,20):
    print (Col[i])
