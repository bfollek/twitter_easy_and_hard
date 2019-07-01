#!/usr/bin/env python3

import os
import requests
from requests_oauthlib import OAuth1

from oauth_builder import OauthBuilder
from random_string import RandomString

CONSUMER_KEY = os.environ["TWITTER_TEST_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
URL = "https://api.twitter.com/1.1/statuses/update.json"


def send_tweet(status):
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    r = requests.post(URL, data={"status": status}, auth=auth)
    return r.status_code


def send_tweet_hard(status):
    request_params = {"status": status}
    oa = OauthBuilder(
        "post",
        URL,
        request_params,
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
    )
    headers = {"authorization": oa.authorization_header()}
    r = requests.post(URL, data=request_params, headers=headers)
    return r.status_code


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        status = f"{sys.argv[1]} {RandomString.make()} {RandomString.make()}"
        print(f"Tweeting {status}")
        rv = send_tweet(status)
        if rv == 200:
            print("Success!")
        else:
            print(f"Bad status: {rv}")
        status = f"{sys.argv[1]} {RandomString.make()} {RandomString.make()}"
        print(f"Tweeting {status}")
        rv = send_tweet_hard(status)
        if rv == 200:
            print("Success!")
        else:
            print(f"Bad status: {rv}")
    else:
        print("You forgot the tweet!")
