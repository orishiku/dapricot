import tweepy

class TwitterHandler(object):
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.__auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.__auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(self.__auth)
    
    def get_account_data(self):
        pass