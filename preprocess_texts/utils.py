import re
import os
import sys
import pandas as pd
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
from bs4 import BeautifulSoup
from textblob import TextBlob
import unicodedata

nlp = spacy.load("en_core_web_sm")
#nlp = en_core_web_sm.load()

def _get_wordcounts(x):
    wordlength = len(str(x).split())
    return wordlength + len(str(x))

def _get_charcounts(x):
    value = x.split()
    x = ''.join(value) 
    return len(x) 

def _get_avg_wordcount(x):
     count = _get_charcounts(x)/_get_wordcounts(x)
     return count

def _get_stopwords_count(x):
    return len([t for t in x.split() if t in stopwords])
     

def _get_hashtag_count(x):
    return len([t for t in x.split() if t.startswith('#')])
     

def _get_mention_count(x):
    return len([t for t in x.split() if t.startswith('@')])
    

def _get_digit_count(x):
    return  len([t for t in x.split() if t.isdigit()])

def _get_uppercaset_count(x):
    return  len([t for t in x.split() if t.isupper()])

def _cont_extraction(x):
    contractions = {
        "ain't":"am not",
        "aren't":"are not",
        "can't":"can not",
        "can't've":"can not have",
        "cause":"because",
        "b'coz":"because",
        "could've":"could have",
        "couldn't've":"could not have",
        "didn't":"did not",
        "doesn't":"does not",
        "don't":"do not",
        "hadn't":"had not",
        "hadn't've":"had not have",
        "hasn't":"has not",
        "haven't":"have not",
        "he'd":"he would",
        "he'd've":"he would have",
        "he'll":"he will",
        "he'll've":"he will have",
        "he's":"he is",
        "how'd":"how did",
        "how'd'y":"how do you",
        "how'll":"how will",
        "how's":"how does",
        "i'd":"I would",
        "I'd":"I would",
        "i'd've":"I would have",
        "I'd've":"I would have",
        "i'll":"I will",
        "I'll":"I will",
        "i'll've":"I will have",
        "I'll've":"I will have",
        "i'm":"I am",
        "I'm":"I am",
        "i've":"I have",
        "I've":"I have",
        "isn't":"isn't",
        "it'd":"it would",
        "it'd've":"it would have",
        "it'll":"it will",
        "it'll've":"it will have",
        "it's":"it is",
        "let's":"let us",
        "ma'am":"madam",
        "m'am":"madam",
        "mayn't":"may not",
        "might've":"might have",
        "mightn't":"might not",
        "mightn't've":"might not have",
        "must've":"must have",
        "mustn't":"must not",
        "mustn't've":"must not have",
        "needn't":"need not",
        "needn't've":"need not have",
        "o'clock":" of the clock",
        "oughtn't":"ought not",
        "oughtn't've":"ought not have",
        "shan't":"shall not",
        "sha'n't":"shall not",
        "shan't've":"shall not have",
        "she'd":"she would",
        "she'd've":"she would have",
        "she'll":"she will",
        "she'll've":"she will have",
        "she's":"she is",
        "should've":"should have",
        "shouldn't":"should not",
        "shouldn't've":"should not have",
        "so've":"so have",
        "so's":"so is",
        "that'd":"that would",
        "that'd've":"that would have",
        "that's":"that is",
        "there'd":"there would",
        "there'd've":"there would have",
        "there's":"there is",
        "they'd":"they would",
        "they'd've":"they would have",
        "they'll":"they will",
        "they'll've":"they will have",
        "they're":"they will",
        "they've":"they have",
        "to've":"to have",
        "wasn't":"was not",
        " u ":" you ",
        " ur ": " your ",
        " n " :  " and ",
        "won't":"would not",
        "dis":"this",
        "bak":"back",
        "brng":"bring"
    }

    if type(x) is str:
        for key in contractions:
            value = contractions[key]
            x=x.replace(key,value)
        return x
    else:
        return x
    
def _get_emails(x):
    emails = re.findall(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+._-]+\b)',x)
    emails_count = len(emails)
    return emails_count, emails

def _remove_emails(x):
    return re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+._-]+)','',x)

def _get_urls(x):
    urls = re.findall(r'(http|https|ftp|ssh):([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w.,@?^=%&:/~+#-])?',x)
    urls_count = len(urls)
    return urls_count, urls

def _remove_urls(x):
    return re.sub(r'(http|https|ftp|ssh):([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w.,@?^=%&:/~+#-])?','',x)

def _remove_rt(x):
     return re.sub(r'\brt\b','',x).strip()

def _remove_specialchars(x):
    x = re.sub(r'[^\w ]+','',x)
    x = ' '.join(x.split())
    return x

def _remove_htmltags(x):
    return BeautifulSoup(x,'lxml').get_text().strip()

def _remove_accented_chars(x):
    return unicodedata.normalize('NFKD',x).encode('ascii')

def _remove_stopwords(x):
    return ' '.join([t for t in x.split() if t not in stopwords])

def _make_base(x):
    x = str(x)
    x_list=[]
    doc = nlp(x)

    for token in doc:
        lemma = token.lemma_
        if lemma == '-PRON-' or lemma == 'be':
            lemma = token.text

        x_list.append(lemma)
    return ' '.join(x_list)     

def _get_value_counts(df,col):
    text = ' '.join(df[col])
    text = text.split()
    freq = pd.Series(text).value_counts()
    return freq


def _remove_commonwords(x, freq, no=20):
    fno = freq[:no]  
    x = ' '.join([t for t in x.split() if t not in fno ])
    return x

def _remove_rarewords(x, freq, no = 20):
    fno = freq.tail(no)
    x = ' '.join([t for t in x.split() if t not in fno ])
    return x

def _spelling_correction(x):
    x = TextBlob(x).correct()
    return x






 