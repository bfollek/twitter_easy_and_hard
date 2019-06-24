#!/usr/bin/env python3

import os

from twython import Twython, TwythonError

from random_string import RandomString

URL = "https://api.twitter.com/1.1/statuses/update.json"


def send_tweet(status):
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    try:
        response = twitter.update_status(status=status)
        return None
    except TwythonError as e:
        return f"Error {e.error_code}: {e}"


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        status = f"{sys.argv[1]} {RandomString.make()} {RandomString.make()}"
        print(f"Tweeting {status}")
        s = send_tweet(status)
        if s:
            print(s)
        else:
            print("Success!")
    else:
        print("You forgot the status!")
