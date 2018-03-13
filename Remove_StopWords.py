import io
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#word_tokenize accepts a string as an input, not a file.
wordlist=["one","im","would","also","ive","lol"]
stop_words = set(stopwords.words('english'))
file1 = open("C:\TuDiabetes_Code\Diabetes_Text_New\All.txt")
line = file1.read()# Use this to read file content as a stream:
words = line.split()
for r in words:
    if not r in stop_words:
        appendFile = open('C:\TuDiabetes_Code\Diabetes_Text_New\CleanText.txt','a')
        appendFile.write(" "+r)
        appendFile.close()

lemma = WordNetLemmatizer()
exclude = set(string.punctuation)
stoplist= stopwords.words('english')
stoplist= stoplist+wordlist

stop = set(stoplist)
# stop= stop.append
# print type(stop)
# print(stop)
# exit(0)
stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
return normalized