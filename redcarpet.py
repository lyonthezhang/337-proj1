import re
import nltk
import numpy as np
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import sys

from collections import Counter
from fuzzywuzzy import fuzz
import spacy

def remove_symbols(a_tweet):
	entity_prefixes = ['@','#']
	words = []
	for word in a_tweet.split():
		word = word.strip()
		if word:
			if word[0].lower() not in entity_prefixes:
				words.append(word)
	return ' '.join(words)

def noisefilter(tweet):
	ban_list = ['rt','golden','globes']
	for i in ban_list:
		tweet = tweet.replace(i,'')
	return tweet

def get_people(scores):
	best = []
	worst = []
	
	for k, v in scores.items():
	    best.append((v[0], k))
	    worst.append((v[1], k))
	
	b = sorted(best, key = lambda x: x[0], reverse = True)
	w = sorted(best, key = lambda x: x[0])

	best_names = [t[1] for t in b]
	worst_names = [t[1] for t in w]

	return best_names[:3], worst_names[:3]

def run_redcarpet(year):
	nlp = spacy.load("en_core_web_sm")
	with open('gg' + str(year) + '.json') as jsonfile:
		data = json.load(jsonfile)
	worstre = 'worst dressed'
	bestre = 'best dressed'
	wtweets = []
	btweets = []

	tweets = data
	for i in tweets:
		tweet = remove_symbols(i['text'].lower())
		worstresult = re.search(worstre, tweet)
		bestresult = re.search(bestre, tweet)
		if worstresult and bestresult:
			continue
		elif worstresult:
			wtweets.append(noisefilter(tweet))
		elif bestresult:
			btweets.append(noisefilter(tweet))

	dress_score_dict = {}
	#format for values will be [bestcount, worstcount]
	for i in wtweets:
		result = nlp(i)
		pair_flag = False
		person_name = ''
		for token in result:
			if token.ent_type_ == "PERSON" and pair_flag == False:
				pair_flag = True
				person_name = token.text + ' '
			elif token.ent_type_ == "PERSON" and pair_flag == True:
				pair_flag = False
				person_name += token.text
				if person_name not in dress_score_dict.keys():
					dress_score_dict[person_name] = [0,1]
				else:
					dress_score_dict[person_name][1] += 1
	for i in btweets:
		result = nlp(i)
		pair_flag = False
		person_name = ''
		for token in result:
			if token.ent_type_ == "PERSON" and pair_flag == False:
				pair_flag = True
				person_name = token.text + ' '
			elif token.ent_type_ == "PERSON" and pair_flag == True:
				pair_flag = False
				person_name += token.text
				if person_name not in dress_score_dict.keys():
					dress_score_dict[person_name] = [1,0]
				else:
					dress_score_dict[person_name][0] += 1


	#DRESS_SCORE_DICT FORMAT: {key: person name, value: [best dressed tally, worst dressed tally]}
	top_3_dress, bottom_3_dress = get_people(dress_score_dict)
	
	print("\nThree BEST Dressed: {}\n".format(top_3_dress))
	print("\nThree WORST Dressed: {}\n".format(bottom_3_dress))
	
	print(dress_score_dict)

if __name__ == "__main__":
	result = run_redcarpet(sys.argv[1])
