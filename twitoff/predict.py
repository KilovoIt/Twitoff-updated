import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, tweet_text):
     user0 = User.query.filter(User.name == user0_name).one()
     user1 = User.query.filter(User.name == user1_name).one()
     user0_vects = np.array([tweet.vect for tweet in user0.tweets])
     user1_vects = np.array([tweet.vect for tweet in user1.tweets])

     vects = np.vstack([user0_vects, user1_vects])

     labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))], axis=1)
     logistic_regression = LogisticRegression().fit(vects, labels)
     vect_tweet_text = vectorize_tweet(tweet_text).reshape(1, -1)
     return logistic_regression.predict(vect_tweet_text)


