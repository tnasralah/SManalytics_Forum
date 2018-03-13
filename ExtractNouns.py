from textblob import TextBlob
txt = "Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned with the inter"
blob = TextBlob(txt)
print(' '.join(blob.noun_phrases))

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

print(stemmer.stem('working today'))


