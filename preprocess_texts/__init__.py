from preprocess_texts import utils

__version__ ="0.0.1"

def get_wordcounts(x):
    return utils._get_avg_wordcount(x)

def get_charcounts(x):
    return utils._get_charcounts(x)

def get_avg_wordcount(x):
    return utils._get_avg_wordcount(x)

def get_stopwords_count(x):
    return utils._get_stopwords_count(x)

def get_hashtag_count(x):
    return utils._get_hashtag_count(x)

def get_mention_count(x):
    return utils._get_mention_count(x)

def get_digit_count(x):
    return utils._get_digit_count(x)

def get_uppercaset_count(x):
    return utils._get_uppercaset_count(x)

def cont_extraction(x):
    return utils._cont_extraction(x)

def get_emails(x):
    return utils._get_emails(x)

def remove_emails(x):
    return utils._remove_emails(x)

def get_urls(x):
    return utils._get_urls(x)

def remove_urls(x):
    return utils._remove_urls(x)

def remove_rt(x):
    return utils._remove_rt(x)

def remove_specialchars(x):
    return utils._remove_specialchars(x)

def remove_htmltags(x):
    return utils._remove_htmltags(x)

def remove_accented_chars(x):
    return utils._remove_accented_chars(x)

def remove_stopwords(x):
    return utils._remove_stopwords(x)

def make_base(x):
    return utils._make_base(x)

def get_value_count(df,col):
    return utils._get_value_count(df,col)

def remove_commonwords(x, freq, no=20):
    return utils._remove_commonwords(x, no)

def remove_rarewords(x, freq, no = 20):
    return utils._remove_rarewords(x, no)

def spelling_correction(x):
    return utils._spelling_correction(x)
