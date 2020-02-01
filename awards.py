import re
import nltk
import numpy as np
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from collections import Counter
from fuzzywuzzy import fuzz

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


def remove_symbols(a_tweet):
    entity_prefixes = ['@','#']
    words = []
    for word in a_tweet.split():
        word = word.strip()
        if word:
            if word[0].lower() not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

with open('gg2013.json') as jsonfile:
	data = json.load(jsonfile)

regexp = "best"
stopregexp = ":|-|goes to|goes|\bfor"
tweets_with_best = []
whole_tweets_with_best = []

tweets = data[80001:100000]
text = []
for i in tweets:
	tweet = remove_symbols(i['text'].lower())
	result = re.search(regexp, tweet)
	if result:
		after_best = tweet[result.span()[0]:min(result.span()[1]+50,len(tweet) - 1)]
		stopspot = re.finditer(stopregexp, after_best)
		stopspot = [x for x in stopspot]
		if stopspot:
			stop_point = stopspot[-1]
			after_best = after_best[0:stop_point.span()[0]]
		if len(after_best) > 20:
			tweets_with_best.append(after_best)
		whole_tweets_with_best.append(tweet)

for i in tweets_with_best:
	print(i)

# awards = []
# counter = 0
# for i in tweets_with_best:
# 	print(counter)
# 	counter += 1
# 	need_new = True
# 	for j in awards:
# 		if fuzz.partial_ratio(j[0],i) > 85:
# 			j[1] += 1
# 			need_new = False
# 	if need_new and len(awards) < 50:
# 		awards.append([i,1])
# 	elif need_new and len(awards) >= 50:
# 		awards.sort(key=lambda x: x[1])
# 		awards[0] = [i,1]







