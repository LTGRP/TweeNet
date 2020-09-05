import sys
import tweepy
from keys import key

API_KEY = key['api_key']
API_SECRET = key['api_secret']
ACCESS_TOKEN = key['access_token']
ACCESS_TOKEN_SECRET = key['access_token_secret']

target = "NASA"  # target account screen name

try:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True,
                     compression=True)

    friends_list = []
    for page in tweepy.Cursor(api.friends_ids, screen_name=target).pages():
        friends_list += page

    for sid in friends_list:
        for tid in friends_list:
            if sid != tid:
                # friendship between two account
                friendship = api.show_friendship(source_id=sid, target_id=tid)
                if friendship[0].following:
                    print(sid, '-->', tid, '(friends)')
                else:
                    print(sid, '-->', tid, '(not friends)')


except tweepy.TweepError:
    print("tweepy.TweepError=", tweepy.TweepError)

except Exception:
    e = sys.exc_info()[0]
    print("Error: %s" % e)
