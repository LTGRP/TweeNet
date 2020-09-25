import json
import tweepy
import click
from keys import key


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


@click.command()
@click.argument('target')
@click.option('-f', '--filename',
              default='data.json',
              show_default=True,
              help='filename of output data')
def fetch_data(target, filename):
    auth = tweepy.OAuthHandler(key['api_key'], key['api_secret'])
    auth.set_access_token(key['access_token'], key['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True,
                     compression=True)
    try:
        target_info = api.get_user(screen_name=target)
    except tweepy.TweepError as e:
        print(e)
        exit()

    result = {}
    print('Fetching target\'s friend list...' )
    result[target] = lookup_friend_list(api, target_info.id)
    total = len(result[target])
    print(str(total) + " friends finded.")

    for i, user in enumerate(result[target]):
        print("Looking up " + user["screen_name"] + "'s friends (" + str(i+1) + "/" + str(total) + ")")
        result[user["screen_name"]] = lookup_friend_list(api, user["id"])

    with open(filename, 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    fetch_data()
