from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("my_model/")

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    try:
        """retrieving the data from twitter via tweepy"""
        twitter_user = TWITTER.get_user(username)
        """creating a DB user if it does not exist"""
        db_user = (User.query.get(twitter_user.id)) or (User(id=twitter_user.id, name=username))
        
        """Adding a user to the database"""
        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended', since_id=db_user.newest_tweet_id)

        if tweets:
            """if tweets exist, the newest tweet will be #1, or under the index of 0"""
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error Processing {}: {}".format(username, e))
        raise e
    else:
        DB.session.commit()


def update_all_users():
    for user in User.query.all():
        add_or_update_user(user.name)

def insert_example_users():
    add_or_update_user('elonmusk')
    add_or_update_user('AOC')


    
