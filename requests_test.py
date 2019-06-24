#!/usr/bin/env python3

import os

import requests

from random_string import RandomString

URL = "https://api.twitter.com/1.1/statuses/update.json"

# Good info here: what goes in the header, how to build it, etc.
# https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request.html

def send_tweet(status):
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    try:
        response = twitter.update_status(status=status)
        #response.status_code
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        status = f"{sys.argv[1]} {RandomString.get()} {RandomString.get()}"
        print(f"Tweeting {status}")
        s = send_tweet(status)
        if s:
            print(s)
        else:
            print("Success!")
    else:
        print("You forgot the status!")
