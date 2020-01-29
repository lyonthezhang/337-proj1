import pandas as pd
from statistics import mode
import spacy
import json

# remove symbols from tweets
def remove_symbols(a_tweet):
    entity_prefixes = ['@','#']
    words = []
    for word in a_tweet.split():
        word = word.strip()
        if word:
            if word[0].lower() not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

# load tweet data
def get_tweet_data(year):
    if (year == 2020):
        return pd.read_json('gg2020.json', lines = True)
    file_string = 'gg' + str(year) + '.json'
    tweets = {}
    with open(file_string, 'r') as f:
        tweets = json.load(f)
    tweets = [tweet['text'] for tweet in tweets] # extract 'text' field from tweets
    # remove @... tokens
    tweets = [remove_symbols(tweet) for tweet in tweets]
    df = pd.DataFrame(tweets, columns = ['text'])
    return df

# load data
data_2013 = get_tweet_data(2013)
data_2015 = get_tweet_data(2015)
data_2020 = get_tweet_data(2020)

# return list of 'PERSON' in tweet
def get_person(tweet):
    words = [(ent.text, ent.label_) for ent in tweet.ents]
    return ([token[0] for token in list(filter(lambda x: "PERSON" in x, words))])

# return string name of host(s)
def get_hosts(data):
    nlp = spacy.load("en_core_web_sm")

    host_data = data[data['text'].str.contains("host")] # get tweets with 'host' in text
    host_df = host_data[host_data["text"].str.contains("next year") == False] # remove tweets with 'next year'
    host_df['full names'] = host_df['text'].apply(lambda x: get_person(nlp(x))) # id 'PERSON' in tweets
    host_table = host_df[host_df['full names'].str.len() != 0] # remove rows with no 'PERSON'

    # get most mentioned 'PERSON'
    hosts = host_table['full names'].value_counts().argmax()

    return hosts

def run_hosts(year):
    data = get_tweet_data(year)
    hosts = get_hosts(data)
    return hosts
