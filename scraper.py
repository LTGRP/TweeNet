import sys
import time
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

target = "SpaceX"  # target account screen name
target_info = api.get_user(screen_name=target)


def connection_handler(cursor):
    # handle connection error when retrying requests
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError as e:
            print(e)
        except StopIteration:
            break


def lookup_friend_list(api, id):
    adjacency_list = []
    for friend in connection_handler(tweepy.Cursor(api.friends, id=id).items()):
        user_info = {
                "id": friend.id,
                "screen_name": friend.screen_name,
            }
        adjacency_list.append(user_info)
    return adjacency_list


result = {}
result[target] = lookup_friend_list(api, target_info.id)

total = len(result[target])
for i, user in enumerate(result[target]):
    print("Looking up " + user["screen_name"] + "'s friends (" + str(i+1) + "/" + str(total) + ")")
    result[user["screen_name"]] = lookup_friend_list(api, user["id"])

with open('data.json', 'w') as f:
    json.dump(result, f, indent=4)
