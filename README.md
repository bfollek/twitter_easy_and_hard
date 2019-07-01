# twitter_easy_and_hard

Different approaches to sending a tweet in python.

#### The Easy Tweet

Use [Twython](https://github.com/ryanmcgrath/twython). For production code, this is the way to go. I did this in twython_way.py.

#### The Somewhat Harder Way

Use [Requests](https://2.python-requests.org/en/master/). This is a lower-level approach. You have to explicitly set the Twitter API URL and the request params. On the plus side, you can take advantage of the OAuth1() helper that Requests provides. I did this in the send_tweet() function in requests_way.py.

#### The Much Harder, Much More Interesting Way

Use [Requests](https://2.python-requests.org/en/master/), and don't use the OAuth1() helper. Create the OAuth authorization header yourself. I did this in the send_tweet_hard() function in requests_way.py.

So what's the point? I got curious about the magic. I pass in the four magic values:

* consumer_key
* consumer_secret
* access_token
* access_token_secret

and OAuth is happy. But how? Why? How does it work?

These Twitter specs lay out the magic:

* [Authentication](https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request.html)
* [Signature](https://developer.twitter.com/en/docs/basics/authentication/guides/creating-a-signature.html)

Lots of steps, lots of detail, but nothing really daunting. So I coded it up in oauth_builder.py. No more mystery, and I now have some understanding and appreciation of what OAuth does:

* The shared secrets don't leave the sender. The sender uses them as input to a hash, along with a bunch of other public stuff. The hash travels, along with its public pieces. The receiver grabs its own local values for the secrets, adds the public pieces it received, and builds its own version of the hash. If the secrets don't match, the hashes won't match, and the request isn't authorized.

* The public pieces are a bunch of OAuth values and the details of the request: http method, url, and parameters. If someone tampers with the request in transit and changes any of these, the hashes won't match, and the request isn't authorized.

So there are two levels of security:
* Shared secrets
* A tamper-resistant message

I'm not a crypto/security person, but this feels pretty robust.
