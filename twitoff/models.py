from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Tweet Table using SQLAlchemy syntax
class Tweet(DB.Model):
    """Twitter Tweets that corresspond to users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    """Tweet text"""
    text = DB.Column(DB.Unicode(300))
    """Vectorized data field"""
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)
    """Backref that connects tweet to a corresponding user"""
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: '{}'>".format(self.text)
    
# def insert_example_users():
#     """Will get error ran twice, data to play with"""
#     nick = User(id=1, name="nick")
#     elonmusk = User(id=2, name="elon musk")
#     DB.session.add(nick)
#     DB.session.add(elonmusk)
#     DB.session.commit()