import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from datetime import datetime

#nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
stop_words = set(stopwords.words('english'))
topic_stop_words = {"boston", "like", "take", "want", "thing", "well", "http", "https","com", "thank", "yall", "come", "back", "look", "nice","place", "good", "best", "stuff", "also", "reddit", "comment", "sidebar"}
#stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()

def get_utc_from_month_year(month,year):
    return datetime(year,month,1)
def get_utc_from_now():
    return datetime.now()
def get_date_from_utc(utc):
    return datetime(utc)
def get_date_from_now():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
def get_stopwords():
    return stop_words

def get_topic_words(input):
    temp = input.split()
    output=[x for x in temp if x not in topic_stop_words]
    return output

def getKeyWordsFromString(input):
    cleanStr = getStringLettersNumbers(input)
    cleanStr = tokenizeWords(cleanStr,3)  

    #all lower case
    cleanStrSmall = cleanStr.lower()
    return cleanStrSmall
def getHyperlinksFromString(input):
    #cleanStr = re.findall(r'\[.+\]\(.+\)',input)
    cleanStr = re.findall(r'\[[^]]+\]\([^)]+\)',input)
    return cleanStr
def getStringLettersNumbers(input):
    #remove everything except alphabets
    #print(type(input))
    cleanStr = re.sub(r'\(.+\)'," ",input)
    cleanStr = re.sub("[^a-zA-Z#]", " ", cleanStr)
    return cleanStr
def sanitizeURL(input):
    cleanStr = re.sub(r'[,]'," ",input)
    return cleanStr
def tokenizeWords(input, wordsize):
    #remove short words (less than 5 letters)
    listStr = input.split()
    output=""
    #plurals = [stemmer.stem(listStr) for listStr in listStr]
    plurals = [wordnet_lemmatizer.lemmatize(word, pos="v") for word in listStr]
    output=output.join(x+" " for x in plurals if (len(x)>wordsize and not x in stop_words))
    return output

def separate_by_class(dataset):
    separated=dict()
    for i in range(len(dataset)):
        vector = dataset[i]
        class_value = vector[0]
        if(class_value not in separated):
            separated[class_value] = list()
        separated[class_value].append(vector)
    return separated
def column(matrix, i):
    return [row[i] for row in matrix]

