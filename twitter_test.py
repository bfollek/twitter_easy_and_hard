#!/usr/bin/env python3

URL = "https://api.twitter.com/1.1/statuses/update.json"


def send_tweet(status):
    print(status)
    return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        status = sys.argv[1]
        print(f"Status: {send_tweet(status)}")
