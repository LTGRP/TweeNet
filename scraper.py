import sys
import json
import tweepy
from keys import key

API_KEY = key['api_key']
API_SECRET = key['api_secret']
ACCESS_TOKEN = key['access_token']
ACCESS_TOKEN_SECRET = key['access_token_secret']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 compression=True)

target = "NASA"  # target account screen name
target_info = api.get_user(screen_name=target)

adjacency_list = {}
adjacency_list[target_info.id] = []

try:
    for page in tweepy.Cursor(api.friends_ids, id=target_info.id).pages():
        adjacency_list[target_info.id] += page

    for uid in adjacency_list[target_info.id]:
        adjacency_list[uid] = []
        for page in tweepy.Cursor(api.friends_ids, id=uid).pages():
            adjacency_list[target_info.id] += page

    with open('data.json', 'w') as f:
        json.dump(adjacency_list, f, indent=4)

except tweepy.TweepError:
    print("tweepy.TweepError=", tweepy.TweepError)

except Exception:
    e = sys.exc_info()[0]
    print("Error: %s" % e)
