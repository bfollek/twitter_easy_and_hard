#!/usr/bin/env python3

import os
import random
import string

from twython import Twython

URL = "https://api.twitter.com/1.1/statuses/update.json"


def send_tweet(status):
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    twitter.update_status(status=status)


def _random_string(size=16, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        status = f"{sys.argv[1]} {_random_string()} {_random_string()}"
        print(f"Tweeting {status}")
        send_tweet(status)
