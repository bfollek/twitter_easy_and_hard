#!/usr/bin/env python3

import os
import requests
from requests_oauthlib import OAuth1

from oauth_builder import OauthBuilder
from random_string import RandomString


def send_tweet(status):
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    url = "https://api.twitter.com/1.1/statuses/update.json"
    r = requests.post(url, data={"status": status}, auth=auth)
    return r.status_code


def send_tweet2(status):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    request_params = {"status": status}
    consumer_key = os.environ["TWITTER_TEST_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_TEST_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_TEST_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_TEST_ACCESS_TOKEN_SECRET"]
    oa = OauthBuilder(
        "post",
        url,
        request_params,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    )
    headers = {"authorization": oa.authorization_header()}
    r = requests.post(url, data=request_params, headers=headers)
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
        rv = send_tweet2(status)
        if rv == 200:
            print("Success!")
        else:
            print(f"Bad status: {rv}")
    else:
        print("You forgot the tweet!")
