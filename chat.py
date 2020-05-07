import nltk
import string
import random
import re
import warnings
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer

warnings.filterwarnings("ignore")  #ignore any warning that come up

f=open('atul.txt','r', errors='ignore')  #opening the corpus
raw=f.read()  #reading the corpus

raw=raw.lower()  #converting the whole corpus to lowercase
sent_tokens=raw.split(".")

#sent_tokens=nltk.sent_tokenize(raw)  #sentence tokenization
word_tokens=nltk.word_tokenize(raw)  #word tokenization

lemmer=nltk.stem.WordNetLemmatizer()
stemmer=PorterStemmer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

greeting_inputs = ["hello", "hi", "greetings", "sup", "what's up","hey"]
greeting_responses = ["Hi! How can I help you?", "*nods*", "Hi there! How can I help you?", "Hi! I'd be glad to help you out"]

def greeting(sentence):
    
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)
        
        
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def response(user_response,q):
    
    robo_response=''
    sent_tokens.append(user_response)
    
  
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    
    tfidf = TfidfVec.fit_transform(sent_tokens)   
    tfidf_q = TfidfVec.transform(q)   
    
    vals = cosine_similarity(tfidf_q, tfidf)  
    
    idx1=vals.argsort()[0][-2]
    idx2=vals.argsort()[0][-3]
    
    flat = vals.flatten()

    flat.sort()

    req_tfidf = flat[-2]    
    
    if(req_tfidf==0):
        robo_response=robo_response+"I'm sorry, I'm unable to understand you. "
        return robo_response
    else:
        robo_response = robo_response + str(sent_tokens[idx1]).capitalize()+"."
        return robo_response
    
def words(query):

    query_words=nltk.word_tokenize(query)
    query_lem_words=LemTokens(query_words)
    query_pos_tag=nltk.pos_tag(query_lem_words)
    print(query_pos_tag)
    types=['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB', 'RBS', 'RBR', 'RB' ,'NN', 'NNP', 'NNS', 'LS', 'JJ', 'JJR', 'JJS', 'CD']
    
    filtered_words=[]
    
    for i in query_pos_tag:
        if i[1] in types:
            filtered_words.append(i)
    
    return filtered_words

def check_synonyms(question):
    
    filtered_words_tuples=words(question) #filtered list of tuples of (best words,form) from question asked
    
    filtered_words_list=[i[0] for i in filtered_words_tuples] #list of best words
    print(filtered_words_list)
    
    synonyms=[]
    
    for i,j in filtered_words_tuples:
        s = [] 
        for syn in wordnet.synsets(i): 
            for l in syn.lemmas(): 
                s.append(l.name()) 
        synonyms.append(s)
    
    similar_quests=[]
    for i in filtered_words_list:
        for j in synonyms:
            for k in j:
                s=question.replace(i,k)
                similar_quests.append(s)
    similar_quests = list(dict.fromkeys(similar_quests))
    return similar_quests
    
def clean(x):
    x=[re.sub('[^A-Za-z0-9]+', ' ', i) for i in x]
    x=[i.strip() for i in x]
    return x

def quest(question):
    question=question.lower()
    val=greeting(question)
    if val!=None:    
        return val
    else:
        f=check_synonyms(question)
        resp=response(question,f)
        resp=resp.strip()
        return resp.capitalize()


