import tweepy
import credentials
import re

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_KEY, credentials.ACCESS_SECRET)
api = tweepy.API(auth)

##Taken from https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b, updated in comments my saaranshM

def deEmojify(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"     # emoticons
                               u"\U0001F300-\U0001F5FF"     # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"     # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"     # flags (iOS)
                               u"\U00002500-\U00002BEF"     # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"                    # dingbats
                               u"\u3030"
                               u"\u2066-\u2069"             # these kept popping up - directional isolates?
                               u"\u203c"                    # double exclamation mark
                               u"\u20a6"                    # Naira sign
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                Output = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                Output = status.retweeted_status.text
        else:
            try:
                Output = status.extended_tweet["full_text"]
            except AttributeError:
                Output = status.text


        #gets rid of hyperlinks and unwanted 
        cleanOutput = ' '.join(re.sub("(@[A-Za-z0-9+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", Output).split())

        cleanOutput = deEmojify(cleanOutput)
        print(cleanOutput)
        f = open("tweetDump.txt", 'a')
        f.write(cleanOutput + ",\n")

    def on_error(self, status_code):
        if status_code == 420:
            return False

print("-------------------------STREAMING TWEETS-------------------------")

### SEARCH HERE ###

#Tweets = api.search("coronavirus")
#for tweet in tweets:
#   if tweet.lang == ['en'] and geocode?
#        print(tweet.text)
#        print to file

### STREAM HERE ###
newEars = MyStreamListener()
flow = tweepy.Stream(auth = api.auth, listener = newEars)

keywords = ['coronavirus', 'COVID-19', 'pandemic', 'epidemic', 'corona']

flow.filter(track=keywords, languages = ['en'])