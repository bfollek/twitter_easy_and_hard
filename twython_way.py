#!/usr/bin/env python3

import os

from twython import Twython, TwythonError

from random_string import RandomString


def send_tweet(status):
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    try:
        twitter.update_status(status=status)
        return None
    except TwythonError as err:
        return err


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        status = f"{sys.argv[1]} {RandomString.make()} {RandomString.make()}"
        print(f"Tweeting {status}")
        err = send_tweet(status)
        if not err:
            print("Success!")
        else:
            print(f"Error {err.error_code}: {err}")
    else:
        print("You forgot the tweet!")
