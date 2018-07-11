"""
collect.py
"""

import requests
from bs4 import BeautifulSoup
import twitter
import json
import re
import time
import collections


def assign_twitter_api():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    twitter_api = twitter.Api(consumer_key=consumer_key,
                              consumer_secret=consumer_secret,
                              access_token_key=access_token,
                              access_token_secret=access_token_secret)
    return twitter_api


def getting_top_tv_series(twitter_api):
    try:
        imdb_top_tv_series = requests.get("http://imdb.com/chart/toptv/?ref_=nv_tvv_250_3").text
    except ValueError:
        print("Oops! Seems like you have reached maximum retries, Please try after sometime..")
    soup = BeautifulSoup(imdb_top_tv_series, "lxml")
    count = 1
    all_the_hashtags = []
    all_tv_series_id = []
    all_tv_series_name = []
    print("Analysis would be done on following tv Series")
    for tv_series in soup.find_all("td", "titleColumn"):
        if count > 22:  # change number of shows here
            break
        tv_series_name = re.search(r'\<a href="(.+)"\>([a-zA-Z0-9: ]+)\<\/a\>', str(tv_series))
        if not tv_series_name:
            continue

        related_hashtag, tv_series_id = effective_tv_series_twitter_handle(twitter_api, tv_series_name.group(2))

        if related_hashtag != 'empty':
            all_the_hashtags.append(related_hashtag)
            all_tv_series_id.append(tv_series_id)
            all_tv_series_name.append(tv_series_name.group(2))
            count = count + 1
    all_tweeting_users = storing_the_related_hashtag_tweets(twitter_api, all_the_hashtags, all_tv_series_id,
                                                            all_tv_series_name)
    common_accounts = 0

    for item, count in collections.Counter(all_tweeting_users).items():
        if count > 1:
            common_accounts = common_accounts + 1

    summary = open('summary.txt', 'a')
    summary.write(
        "The number of common twitter handles tweets among all the tv series is " + str(common_accounts) + "\n")
    summary.close()


def effective_tv_series_twitter_handle(twitter_api, tv_series_name):
    list_tv_series_on_twitter = []
    with open('data.txt') as database_of_twitter:
        for line in database_of_twitter:
            details_from_database = str(line).split('|')
            list_tv_series_on_twitter.append(details_from_database)
    tv_series_screen_name, related_hashtag = searching_in_database(list_tv_series_on_twitter, tv_series_name)

    if related_hashtag == 'empty':
        return related_hashtag, tv_series_screen_name
    try:
        twitter_account_tv_series = twitter_api.GetUser(screen_name=tv_series_screen_name)
    except ValueError:
        print("Oops! Seems like you have reached maximum retries, Please try after sometime..")

    time.sleep(2)
    return related_hashtag, twitter_account_tv_series.id


def searching_in_database(list_tv_series_on_twitter, tv_series_name):
    for tv_series in list_tv_series_on_twitter:
        if (str.lower(tv_series[0].replace(' ', '')) == (str.lower(tv_series_name.replace(' ', '')))):
            print(tv_series[1])
            return tv_series[1], tv_series[2]

    return tv_series_name, 'empty'


def storing_the_related_hashtag_tweets(twitter_api, all_the_hashtags, all_tv_series_id, all_tv_series_name):
    try:
        stored_database = open('related_hashtag_tweets.txt', 'w')
        stored_users = open('tweeting_user.txt', 'w')
        tweeted_users = []
        all_tweeting_user = []
        summary = open('summary.txt', 'w')
        summary.write("The number of tv series is " + str(len(all_tv_series_name)) + "\n")

        for i in range(0, len(all_the_hashtags)):
            print("\n")
            print("Getting Tweets for ", all_the_hashtags[i])
            tweeted_users_count = 0
            tweeted_users = []
            related_hashtag_tweets = twitter_api.GetSearch(term=all_the_hashtags[i], count=100)
            for tweet in related_hashtag_tweets:
                if tweet.lang == 'en' and tweet.user.id not in tweeted_users:
                    if tweeted_users_count < 60:
                        tweeted_users.append(tweet.user.id)
                        all_tweeting_user.append(tweet.user.id)
                        relation_between_user_and_tv = str(tweet.user.id) + "," + str(all_tv_series_id[i])
                        stored_users.write(str(relation_between_user_and_tv) + "\n")

                        tweeted_users_count = tweeted_users_count + 1
                        stored_database.write(str(tweet.text) + "\n")
            stored_database.write("|" + str(all_tv_series_name[i]) + "|\n")
            summary.write(
                "The number of tweets related to " + all_tv_series_name[i] + " is " + str(tweeted_users_count) + "\n")
            time.sleep(5)

        summary.close()
        stored_database.close()
        stored_users.close()
    except ValueError:
        print("Oops! Seems like you have reached maximum retries, Please try after sometime..")

    return all_tweeting_user


print("Started on ", str(time.asctime(time.localtime(time.time()))))
try:
    getting_top_tv_series(assign_twitter_api())
    print("Successfully commpleted on ", str(time.asctime(time.localtime(time.time()))))
except ValueError:
    print("Oops! Seems like you have reached maximum retries, Please try after sometime..")
