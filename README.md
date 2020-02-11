# Golden Globes Project
##### Team 13
##### Members: Lyon Zhang, David Zane, Christine Garver

We wrote separate python files for each function called in gg_api.py. We use NLP to find information about the Golden Globe awards (hosts, presenters, winners, nominees, best/worst dressed, overall sentiment). This program should be generalizable to other awards shows.

#### get_hosts:
For get_hosts, we filtered the tweets for the word 'host' and removed tweets that had the phrase 'next year' in it. Then we got the list of people mentioned using Spacy and chose the top 2 most mentioned people.

#### get_awards:
For get_awards, we filtered the tweets for key verbs such as 'best' and 'goes'. Then, we looked for the most common words in the tweets after best (that were not stopwords). We took the most common unique token words and reported those as the awards.

#### get_winners:
For get_winners, we filter tweets for keywords from the specific award. Then we use a dictionary to track the people mentioned in tweets and the number of times they are mentioned. We return the most mentioned people.

#### get_presenters:
For get_presenters, we filtered the tweets for keywords from the specific award. Therefore, we removed stopwords and other words such as 'miniseries' that many people did not use to describe a certain award. Then we filtered the remaining tweets for key presenting verbs, such as: introduce, read, give, announce, etc. Next, we used Spacy to find the full names of people mentioned. In order to prevent from retrieving the winner's name, we made sure the name mentioned came before the key verb because most of the time winners are mentioned after the key verb. After filtering for similarities between the list of remaining names (to make sure we weren't counting nicknames for people as 2 different people), we returned the 2 most mentioned people in the tweets.

#### Extra Functions:
**Red Carpet:**
<br> For red carpet, we return the 3 best dressed and 3 worst dressed people of the night. First we filter for tweets with the words 'best dress' and 'worst dress'. Then we create a dictionary of names and every time a person is mentioned, the counter for best dress or worst dress increments. We return the 3 highest best dress and 3 highest worst dress scores.
<br>
<br>**Sentiment:**
<br> For sentiment, we used the library TextBlob in order to determine how people were tweeting about the awards show. We created linear counters of sentiment from 'ABSOLUTELY HORRENDOUS' to 'ASTRONOMICALLY BEAUTIFULLY WONDERFUL'. We returned the most common sentiment and the average positive and negative scores among the tweets.

#### Python Libraries Imported:
- from textblob import TextBlob
- import json
- import sys
- import time
- import numpy as np
- import pandas as pd
- import re
- import nltk
- from nltk.tokenize import word_tokenize, sent_tokenize
- from nltk.corpus import stopwords
- from nltk.tag import pos_tag
- from collections import Counter
- from fuzzywuzzy import fuzz
- import spacy
- from statistics import mode
- import string
- import difflib
- from scipy import stats
- from spacy.matcher import Matcher
- import math
