from sklearn.feature_extraction.text import TfidfVectorizer, strip_tags
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
import string
import re, itertools
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
from textblob import TextBlob
# txt = "Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned with the inter"
# blob = TextBlob(txt)
# print(' '.join(blob.noun_phrases))

wordlist=["ok","u","00","type","terry","diabetes","diabetes","4" ,"wouldnt", "thats", "one","hello","youre","yeah", "havent", "hey", "okay","terry4", "ah", "um", "dear", "hi","hii","hiii","im","would","also","ive","lol","1","2","dont","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
def clean(doc):
    lemma = WordNetLemmatizer()
    exclude = set(string.punctuation)
    stoplist= stopwords.words('english')
    stoplist= stoplist+wordlist
    stop = set(stoplist)
    # stop= stop.append
    # print type(stop)
    # print(stop)
    # exit(0)

    # Remove punctuation
    normalized = result = re.sub(r"http\S+", "", doc)
    normalized = result = re.sub(r"than\S+", "", normalized)
    normalized = result = re.sub(r"@\S+", "", normalized)
    normalized = re.sub(r'[^\w\s]', '', normalized).replace("  ", " ")
    # Standardize words (remove multiple letters):
    normalized = ''.join(''.join(s)[:2] for _, s in itertools.groupby(normalized))
    normalized = TextBlob(normalized)
    normalized=' '.join(normalized.noun_phrases)
    stop_free = " ".join([i for i in normalized.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    normalized = normalized.lower().strip().replace("\n", " ").replace(".", " ").replace("-", ' ')


    # with open('C:\TuDiabetes_Code - Final\TechTypes_Text_New\Physical_Activity_Clean.txt', 'a') as the_file:
    #     the_file.write(normalized)
    print normalized
    print "********************************************************"
    return normalized


f = open("C:\TuDiabetes_Code - Final\TechTypes_Text_New\Tech-All.txt", 'r')
# create English stop words list

# Create p_stemmer of class PorterStemmer for Lemmatization
txt = ''
doc_complete = []
pList = []
count = 0
for line in f:
    print line
    l = line.strip()
    l=clean(l)
    # strip HTML tags from file

    txt = strip_tags(l)
    doc_complete.append(txt)
    count += 1

# print number of lines
print count

documents = doc_complete

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

true_k = 20
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :15]:
        print ' %s' % terms[ind],
    print