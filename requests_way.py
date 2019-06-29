#!/usr/bin/env python3

import os
import request

from random_string import RandomString


def send_tweet(status):
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    # try:
    #     response = twitter.update_status(status=status)
    #     #response.status_code
    #     return None
    return "TBD"


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
