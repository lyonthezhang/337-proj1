import json
import re
import string
import spacy
from spacy.matcher import Matcher

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords

# Run the 1st time
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def get_tweet_data(year):
    # load tweet data
    file_string = 'gg' + str(year) + '.json'
    tweets = {}
    with open(file_string, 'r') as f:
        tweets = json.load(f)
    
    # extract 'text' field from tweets
    tweets = [tweet['text'] for tweet in tweets]
    
    # remove @,# tokens
    tweets = [remove_symbols(tweet) for tweet in tweets]
    
    return tweets

def remove_symbols(a_tweet):
    entity_prefixes = ['@','#','(',')']
    words = []
    for word in a_tweet.split():
        word = word.strip()
        if word and word.lower() != 'rt':
            if word[0].lower() not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def tweets_contain(category_name, tweets):
    stop_words = set(stopwords.words('english'))
    stop_words.add('-')
    stop_words.add('performance')
    stop_words.add('comedy')
    stop_words.add('television')

    tokens = nltk.word_tokenize(category_name)
    no_stop_words = [w for w in tokens if not w in stop_words] 
    
    regex = r''
    for token in no_stop_words:
        regex += token
        regex += '.*?'
        
#     regex = category_name
    r = re.compile(regex, re.IGNORECASE)
    filtered_list = list(filter(r.search, tweets))
    return filtered_list

def get_NNP(tweets_list):
    NNP_dict = {}
    for tweet in tweets_list:
        tokens = nltk.word_tokenize(tweet)
        tags = nltk.pos_tag(tokens)
        for word in tags:
            if word[1] in ['NNP']:
                name = word[0].lower()
                if name in NNP_dict:
                    NNP_dict[name] += 1
                else:
                    NNP_dict[name] = 1
    return NNP_dict

def get_top_percent(dictionary, percentile):
    if dictionary == {}:
        return []
    max_val = max(dictionary.values())
    threshold = max_val * percentile
    result = []
    for key in dictionary:
        if dictionary[key] > threshold:
            result.append(key)
    return result

def remove_category_tokens(category, pronouns_dict):
    tokens = nltk.word_tokenize(category) + ['rt']
    tokens += ['motion picture', 'golden', 'television series', 'tv series', 'mini-']
    for token in tokens:
        if token in pronouns_dict:
            pronouns_dict[token] = 0
    return pronouns_dict

def get_category_nominees(category, tweets):
    # filter for tweets which contain the category name regex
    category_tweets = tweets_contain(category, tweets)

    # create a dictionary of person names/film titles
    if 'actor' in category or 'actress' in category:
        pronouns_dictionary = get_person_names(list_of_tweets=category_tweets)
    else:
        pronouns_dictionary = get_NNP(category_tweets)

    # remove tokens contained in the category name
    filtered_category_tweets = remove_category_tokens(category, pronouns_dictionary)

    # get pronouns with >some_percentile frequency 
    category_nominees = get_top_percent(filtered_category_tweets, percentile=0.9)
    
    return category_nominees

def run_nominees(year):
    tweets = get_tweet_data(year)
    
    seperator = ' '
    nominees = {}
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    for category_name in OFFICIAL_AWARDS_1315:
        category_nominees_list = get_category_nominees(category_name, tweets)
        category_nominees_string = seperator.join(category_nominees_list)
        nominees[category_name] = category_nominees_string
        print(category_name, ':', category_nominees_string)
    return nominees




def get_film_titles(list_of_tweets):
    '''
    Input: a list of strings
    Returns: a dictionary where keys = film titles, values = number of times references in the list of tweets
    *Compares tweet content to IMDB database of movie/TV titles 
    '''
    titles_dictionary = {}
    for tweet in list_of_tweets:
        title = extract_title(tweet).lower()
        if title:
            if title in titles_dictionary:
                titles_dictionary[name] += 1
            else:
                titles_dictionary[name] = 1
    return titles_dictionary
    
def get_person_names(list_of_tweets):
    '''
    Input: a list of strings
    Returns: a dictionary where keys = actor/actress names, values = number of times the key is references in the list of tweets
    '''
    nlp = spacy.load('en_core_web_sm')
    names_dictionary = {}
    for tweet in list_of_tweets:
        name = extract_full_name(nlp(tweet), nlp)
        if name:
            name = name.lower()
            if name in names_dictionary:
                names_dictionary[name] += 1
            else:
                names_dictionary[name] = 1
    return names_dictionary
    
    
def extract_full_name(nlp_doc, nlp):
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('FULL_NAME', None, pattern)
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        return span.text
