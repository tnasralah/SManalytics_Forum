
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import re, itertools

# Put the file on the same directory of the script and enter filename
f = open("C:\TuDiabetes_Code - Final\StopWordsList.txt", 'r')
# create English stop words list


# Create p_stemmer of class PorterStemmer for Lemmatization
txt = ''
doc_complete = []
StopList = []
count = 0
for line in f:
    l = line.strip()
    l = re.sub(r'[^\w\s]', '', l).replace("  ", "")
    StopList.append(l)
    count += 1
# print number of lines
print count, '\n', StopList