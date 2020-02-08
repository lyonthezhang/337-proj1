# return list of 'PERSON' in tweet
def get_person(tweet):
    words = [(ent.text, ent.label_) for ent in tweet.ents]
    return ([token[0] for token in list(filter(lambda x: "PERSON" in x, words))])

# remove punctuations from string
def removePunctuation(string):
    string = string.replace("...", " ")
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")
    return string

# return index of word in string
def index_tweet(tweet, word):
    tweet = removePunctuation(tweet)
    if word in tweet.lower().split():
        idx = tweet.lower().split().index(word)
        return idx
    else:
        return -1

# filter for keywords
def get_tweets_with_keywords(df, keywords):
    series = df['text']
    col = series.str.contains(keywords)
    df['keyword?'] = col
    new_df = df[df['keyword?'] == True]
    return new_df

# look for tweets with award
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

def get_award_tweets(award, data):
    lst = tweets_contain(award, data['text'])
    df = pd.DataFrame(lst, columns = ['text'])
    return df


# position of NNP compared to 'best'
def position_of_ppl(tweet, person):
    tweet = removePunctuation(tweet).lower()

    ppl = person[0].lower().split()[0]
    ppl_idx = tweet.lower().split().index(ppl)

    best_idx = tweet.lower().split().index('best')

    if (ppl_idx < best_idx):
        return 1
    else:
        return 0

def cecil_position(tweet, person):
    names = ['Cecil B. DeMille Award', 'Cecil B. DeMille', 'Cecil']
    tweet = removePunctuation(tweet).lower()

    print(person[0].lower().split()[0])
    print(tweet)

    ppl = person[0].lower().split()[0]
    ppl_idx = tweet.lower().split().index(ppl)

    best_idx = tweet.lower().split().index('cecil')

    if (ppl_idx < best_idx):
        return 1
    else:
        return 0

# True if looking at cecil award
def get_positions(df, cecil_award = False):
    if (cecil_award):
        df['position'] = df.apply(lambda row: cecil_position(row['text'], row['full names']), axis = 1)
    else:
        df['position'] = df.apply(lambda row: position_of_ppl(row['text'], row['full names']), axis = 1)
    return df[df['position'] == 1]

# get keywords of award
# get keywords of award
def get_keywords_of_award(award):
    or_in_award = False
    a = award
    awards_lst = award.split()
    #print(awards_lst)
    if 'or' in awards_lst: or_in_award = True


    stopWords = set(stopwords.words('english'))
    # remove punctuation marks
    award = award.translate(str.maketrans('', '', string.punctuation))
    #remove stopwords
    award = word_tokenize(award)
    award = [word for word in award if word not in stopwords.words('english')]
    award = [word.lower() for word in award]
    # remove 'best' and 'award'
    if 'best' in award: award.remove('best')
    if 'award' in award: award.remove('award')
    if 'performance' in award: award.remove('performance')
    if 'motion' in award: award.remove('motion')
    if 'picture' in award: award.remove('picture')
    if 'musical' in award: award.remove('musical')
    # join words
    award = " ".join(award)
    #if or_in_award is True: award = award + " or"
    print("old: {} ... after: {}".format(a, award))
    return award

def get_presenters(award, data):
    # start time
    start = time.time()

    # get keywords
    keywords = get_keywords_of_award(award)

    print(keywords)

    # remove RT
    df = data[data["text"].str.contains("RT") == False]

    # remove tweets that don't have award in it
    df = get_award_tweets(keywords, df)

    # only get tweets where a key word shows up
    key_words = re.compile('=read|intoduce|introduced|introduces|reads|present|presents|presented|gave|gives|give|announce|announces|announced', re.IGNORECASE)
    df = get_tweets_with_keywords(df, key_words)

    if (df.shape[0] == 0):
        return "", ""

    #print("Award: {} ... shape {}".format(award, df.shape))

    #return df

    # get df with 'present, gave, etc.'
    df['presents_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'presents'))
    df['presenter_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'presenter'))
    df['presenters_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'presenters'))
    df['presented_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'presented'))
    df['gave_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'gave'))
    df['gives_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'gives'))
    df['give_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'give'))
    df['announces_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'announces'))
    df['announce_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'announce'))
    df['announced_idx'] = df['text'].apply(lambda tweet: index_tweet(tweet, 'announced'))

    #print("\n\nnow look for people\n\n")

    # get list of people in tweets
    nlp = spacy.load("en_core_web_sm")
    df['full names'] = df['text'].apply(lambda x: get_person(nlp(x)))
    df = df[df['full names'].str.len() != 0] # remove rows with no 'PERSON'

    if (df.shape[0] == 0):
        return "", ""

    #print(df)
    # get position of NNP
    if (award == 'cecil b. demille award'):
        df = get_positions(df, True)
    else:
        df = get_positions(df)

    # length of string
    #len(s.split())

    if (df.shape[0] == 0):
        return "", ""

    # get person who is talked about 80% of the time
    presenters = df['full names'].value_counts().argmax()

    # end time
    end = time.time()

    print("Time elapsed: {}".format(end - start))

    return df, presenters

def run_presenters(year):
    data = get_tweet_data(year)
    df, presenters = get_presenters(award, data)
    return presenters
