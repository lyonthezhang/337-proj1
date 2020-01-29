
import json
import re
import string

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
# Run the 1st time
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')




def remove_symbols(a_tweet):
    entity_prefixes = ['@','#']
    words = []
    for word in a_tweet.split():
        word = word.strip()
        if word:
            if word[0].lower() not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def tweets_contain(string, tweets):
    r = re.compile(string, re.IGNORECASE)
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

def get_top_percent(dictionary, percentile=0.75):
    if dictionary == {}:
        return []
    max_val = max(dictionary.values())
    threshold = max_val * percentile
    result = []
    for key in dictionary:
        if dictionary[key] > threshold:
            result.append(key)
    return result

def remove_category_tokens(category, lst):
    tokens = nltk.word_tokenize(category) + ['rt']
    for token in tokens:
        if token in lst:
            lst.remove(token)
    return lst


def get_tweet_data(year):
    # load tweet data
    file_string = 'gg' + str(year) + '.json'
    tweets = {}
    with open(file_string, 'r') as f:
        tweets = json.load(f)
    
    # extract 'text' field from tweets
    tweets = [tweet['text'] for tweet in tweets]
    
    # remove @... tokens
    tweets = [remove_symbols(tweet) for tweet in tweets]
    
    return tweets

def get_category_nominees(category, year, tweets):
    
    # filter for tweets which contain the category name regex
    category_tweets = tweets_contain(category, tweets)

    # create a dictionary of pronoun tokens
    pronouns_dictionary = get_NNP(category_tweets)

    # get pronouns with >some_percentile frequency 
    frequent_pronouns = get_top_percent(pronouns_dictionary, percentile=0.8)

    # remove tokens contained in the category name
    category_nominees = remove_category_tokens(category, frequent_pronouns)
    
    return category_nominees

def run_nominees(year):
    tweets = get_tweet_data(year)
    
    seperator = ' '
    nominees = {}
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    for category_name in OFFICIAL_AWARDS_1315:
        # print(category_name)
        category_nominees_list = get_category_nominees(category_name, year, tweets)
        category_nominees_string = seperator.join(category_nominees_list)
        nominees[category_name] = category_nominees_string
    return nominees
