# SentimentAnalysis
Sentiment Analysis of the finite number of TV shows according to the User's tweets rather than what IMDB rates the shows.

This project analysis the TV shows on the basis of positive and negative tweets posted by Users for the shows using shows HashTags.
It is a four step process :
Initially tweets are collected using the Twitter API in collect.py and saved in a text file.
Second step is to classify them in positive and negative tweets. This is done by first training the machine with tweets which is used as a training data
and then tweets are classified.
Third step includes clustering the tweets as positive and negative tweets for different shows separately.
Fourth step is the summarize this whole process and give us the most positive rated show as per the user tweets.
