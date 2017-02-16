"""
classify.py
"""
import nltk
import re

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(tweets):
    document_words = set(tweets)
    features = {}
    for word in get_word_features(document_words):
        features['contains(%s)' % word] = (word in document_words)
    return features

reviews = []
with open('training.txt') as training_data_set:
        for line in training_data_set:
            reviews.append((line.split('|')[1].strip('\n'), line.split('|')[0]))
tweets = []
for (words, sentiment) in reviews:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

training_set = nltk.classify.util.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

count_negative = 0
count_positive = 0
max_postive_tweets = 0
tv_series_tweets=[]
summary = open('summary.txt','a')

with open('related_hashtag_tweets.txt') as tweets_data_set:
        for tweet in tweets_data_set:
            tv_series_name = re.search(r'^(\|)[a-zA-Z 0-9]+(\|)$',tweet)
            if tv_series_name:
                if max_postive_tweets < count_positive:
                    max_postive_tweets = count_positive
                    most_popular = "The most popular show among twitter user is "+str(tv_series_name.group().strip("|"))
                summary.write("Number of postive tweets for "+str(tv_series_name.group().strip("|"))+" is "+str(count_positive)+"\n")
                summary.write("Number of negative tweets for "+str(tv_series_name.group().strip("|"))+" is "+str(count_negative)+"\n")
                count_negative = 0
                count_positive = 0
                tv_series_tweets=[]
                continue

            if tweet not in tv_series_tweets:
                response = classifier.classify(extract_features(tweet.split()))
                if response == 'negative':
                    count_negative=count_negative+1
                elif response == 'positive':
                    count_positive=count_positive+1
                tv_series_tweets.append(tweet)
        summary.write(most_popular)
        summary.close()
print("Successful")