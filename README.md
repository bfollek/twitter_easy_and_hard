# twitter_easy_and_hard

Different approaches to sending a tweet in python.

#### The Easy Tweet

Use [Twython](https://github.com/ryanmcgrath/twython). For production code, this is the way to go. I did this in twython_way.py.

#### The Somewhat Harder Way

Use [Requests](https://2.python-requests.org/en/master/). This is a lower-level approach. You have to explicitly set the Twitter API URL and the request params. On the plus side, you can take advantage of the OAuth1() helper that Requests provides. I did this in the send_tweet() function in requests_way.py.

#### The Much Harder, Much More Interesting Way

Use [Requests](https://2.python-requests.org/en/master/), and don't use the OAuth1() helper. Create the oauth authorization header yourself. I did this in the send_tweet_hard() function in requests_way.py.
