import string
from time import time
import urllib.parse

from random_string import RandomString


class OauthBuilder:
    """
    https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request.html
    https://developer.twitter.com/en/docs/basics/authentication/guides/creating-a-signature.html
    """

    def __init__(
        self,
        http_method,
        url,
        request_params,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
    ):
        self._oauth_dict = self._init_oauth_dict(
            consumer_key, access_token, request_params
        )
        self._oauth_dict["oauth_signature"] = self._signature(
            http_method, url, request_params, consumer_secret, access_token_secret
        )

    def authorization_header(self):
        """
        To build the header string, imagine writing to a string named DST.

        Append the string “OAuth ” (including the space at the end) to DST.
        For each key/value pair of the 7 parameters listed above:
            Percent encode the key and append it to DST.
            Append the equals character ‘=’ to DST.
            Append a double quote ‘”’ to DST.
            Percent encode the value and append it to DST.
            Append a double quote ‘”’ to DST.
            If there are key/value pairs remaining, append a comma ‘,’ and a space ‘ ‘ to DST.
        """
        pieces = []
        for k, v in self._oauth_dict.items():
            pieces.append(f'{self._percent_encode(k)}="{self._percent_encode(v)}"')
        s = "OAuth " + ", ".join(pieces)
        return s

    def _init_oauth_dict(self, consumer_key, access_token, request_params):
        # Createe the keys in alpha order. The dict will preserve the order.
        d = {}
        d["oauth_consumer_key"] = consumer_key
        # "...any approach which produces a relatively random alphanumeric string should be OK here."
        d["oauth_nonce"] = RandomString.make(chars=string.ascii_letters + string.digits)
        d["oauth_signature"] = None  # Placeholder to get the order right
        d["oauth_signature_method"] = "HMAC-SHA1"
        # "...the number of seconds since the Unix epoch"
        d["oauth_timestamp"] = str(int(time()))
        d["oauth_token"] = access_token
        # "The oauth_version parameter should always be 1.0 for any request sent to the Twitter API."
        d["oauth_version"] = "1.0"
        return d

    def _percent_encode(self, s):
        return urllib.parse.quote(s.encode("utf-8"), safe="")

    def _signature(
        self, http_method, url, request_params, consumer_secret, access_token_secret
    ):
        """
        """
        sps = self._sig_param_string(request_params)
        sbs = self._sig_base_string(http_method, url, sps)
        return "todo encrypt"

    def _sig_param_string(self, request_params):
        """
        The request parameters and the oauth_* values other than oauth_signature need to be encoded into a single string which will be used later on. The process to build the string is very specific:

        (See _make_sig_dict() for 1. and 2.)
        3. For each key/value pair:
        4. Append the encoded key to the output string.
        5. Append the ‘=’ character to the output string.
        6. Append the encoded value to the output string.
        7. If there are more key/value pairs remaining, append a ‘&’ character to the output string.
        """
        sig_dict = self._sig_dict(request_params)
        pieces = []
        for k, v in sig_dict.items():
            pieces.append(f"{k}={v}")
        s = "&".join(pieces)
        return s

    def _sig_dict(self, request_params):
        """
        1. Percent encode every key and value that will be signed.
        2. Sort the list of parameters alphabetically [1] by encoded key [2].

        [1] Note: The OAuth spec says to sort lexigraphically, which is the default alphabetical sort for many libraries.

        [2] Note: In case of two parameters with the same encoded key, the OAuth spec says to continue sorting based on value. However, Twitter does not accept duplicate keys in API requests.
        """
        # Percent-encode requests params. _oauth_dict is already percent-encoded.
        params_encoded = {
            self._percent_encode(k): self._percent_encode(v)
            for k, v in request_params.items()
        }
        # Put all values together, in alpha key order. Ignore the edge case where a request param key
        # matches one of the oauth keys.
        sig_dict = {}
        keys = sorted(list(params_encoded.keys()) + list(self._oauth_dict.keys()))
        keys.remove("oauth_signature")
        for k in keys:
            if k in params_encoded:
                sig_dict[k] = params_encoded[k]
            else:
                sig_dict[k] = self._oauth_dict[k]
        return sig_dict

    def _sig_base_string(self, http_method, url, sig_param_string):
        """
        The three values collected so far must be joined to make a single string, from which the signature will be generated. This is called the signature base string by the OAuth specification.

        To encode the HTTP method, base URL, and parameter string into a single string:

        1. Convert the HTTP Method to uppercase and set the output string equal to this value.
        2. Append the ‘&’ character to the output string.
        3. Percent encode the URL and append it to the output string.
        4. Append the ‘&’ character to the output string.
        5. Percent encode the parameter string and append it to the output string.
        """
        s = f"{http_method.upper()}&{self._percent_encode(url)}&{self._percent_encode(sig_param_string)}"
        return s


"""

URL = "https://api.twitter.com/1.1/statuses/update.json"

Creating a signature

This page explains how to generate an OAuth 1.0a HMAC-SHA1 signature for a HTTP request. This signature will be suitable for passing to the Twitter API as part of an authorized request, as described in Authorizing a request.

The request used to demonstrate signing is a POST to https://api.twitter.com/1.1/statuses/update.json. The raw request looks like this:

POST /1.1/statuses/update.json?include_entities=true HTTP/1.1
Accept: */*
Connection: close
User-Agent: OAuth gem v0.4.4
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
Host: api.twitter.com

 status=Hello%20Ladies%20%2b%20Gentlemen%2c%20a%20signed%20OAuth%20request%21

Collecting the request method and URL

To produce a signature, start by determining the HTTP method and URL of the request. These two are known when creating the request, so they are easy to obtain.

The request method will almost always be GET or POST for Twitter API requests.
HTTP Method 	POST

The base URL is the URL to which the request is directed, minus any query string or hash parameters. It is important to use the correct protocol here, so make sure that the “https://” portion of the URL matches the actual request sent to the API.
Base URL 	https://api.twitter.com/1.1/statuses/update.json

Collecting parameters

Next, gather all of the parameters included in the request. There are two such locations for these additional parameters - the URL (as part of the querystring) and the request body. The sample request includes a single parameter in both locations:

POST /1.1/statuses/update.json?include_entities=true HTTP/1.1
Accept: */*
Connection: close
User-Agent: OAuth gem v0.4.4
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
Host: api.twitter.com

 status=Hello%20Ladies%20%2b%20Gentlemen%2c%20a%20signed%20OAuth%20request%21

In the HTTP request the parameters are URL encoded, but you should collect the raw values. In addition to the request parameters, every oauth_* parameter needs to be included in the signature, so collect those too. Here are the parameters from Authorizing a request:
status 	Hello Ladies + Gentlemen, a signed OAuth request!
include_entities 	true
oauth_consumer_key 	xvz1evFS4wEEPTGEFPHBog
oauth_nonce 	kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg
oauth_signature_method 	HMAC-SHA1
oauth_timestamp 	1318622958
oauth_token 	370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb
oauth_version 	1.0

These values need to be encoded into a single string which will be used later on. The process to build the string is very specific:

    Percent encode every key and value that will be signed.
    Sort the list of parameters alphabetically [1] by encoded key [2].
    For each key/value pair:
    Append the encoded key to the output string.
    Append the ‘=’ character to the output string.
    Append the encoded value to the output string.
    If there are more key/value pairs remaining, append a ‘&’ character to the output string.

[1] 	Note: The OAuth spec says to sort lexigraphically, which is the default alphabetical sort for many libraries.
[2] 	Note: In case of two parameters with the same encoded key, the OAuth spec says to continue sorting based on value. However, Twitter does not accept duplicate keys in API requests.

The following string will be produced by repeating these steps with the parameters collected above:

Parameter string

include_entities=true&oauth_consumer_key=xvz1evFS4wEEPTGEFPHBog&oauth_nonce=kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1318622958&oauth_token=370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb&oauth_version=1.0&status=Hello%20Ladies%20%2B%20Gentlemen%2C%20a%20signed%20OAuth%20request%21
Creating the signature base string

The three values collected so far must be joined to make a single string, from which the signature will be generated. This is called the signature base string by the OAuth specification.

To encode the HTTP method, base URL, and parameter string into a single string:

    Convert the HTTP Method to uppercase and set the output string equal to this value.
    Append the ‘&’ character to the output string.
    Percent encode the URL and append it to the output string.
    Append the ‘&’ character to the output string.
    Percent encode the parameter string and append it to the output string.

This will produce the following:

Signature base string

POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521

Make sure to percent encode the parameter string! The signature base string should contain exactly 2 ampersand ‘&’ characters. The percent ‘%’ characters in the parameter string should be encoded as %25 in the signature base string.

Getting a signing key

The last pieces of data to collect are secrets which identify the Twitter app making the request, and the user the request is on behalf of. It is very important to note that these values are incredibly sensitive and should never be shared with anyone.

The value which identifies your app to Twitter is called the consumer secret and can be found in the developer portal by viewing the app details page. This will be the same for every request your Twitter app sends.
Consumer secret 	kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw

The value which identifies the account your application is acting on behalf of is called the oauth token secret. This value can be obtained in several ways, all of which are described at Obtaining access tokens.
OAuth token secret 	LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE

Once again, it is very important to keep these values private to your application. If you feel that your values have been compromised, regenerate your tokens (the tokens on this page have been marked as invalid for real requests).

Both of these values need to be combined to form a signing key which will be used to generate the signature. The signing key is simply the percent encoded consumer secret, followed by an ampersand character ‘&’, followed by the percent encoded token secret:

Note that there are some flows, such as when obtaining a request token, where the token secret is not yet known. In this case, the signing key should consist of the percent encoded consumer secret followed by an ampersand character ‘&’.
Signing key 	kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw&LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE

Calculating the signature

Finally, the signature is calculated by passing the signature base string and signing key to the HMAC-SHA1 hashing algorithm. The details of the algorithm are explained hash_hmac function.

The output of the HMAC signing function is a binary string. This needs to be base64 encoded to produce the signature string. For example, the output given the base string and signing key given on this page is 84 2B 52 99 88 7E 88 7602 12 A0 56 AC 4E C2 EE 16 26 B5 49. That value, when converted to base64, is the OAuth signature for this request:
OAuth signature 	hCtSmYh+iHYCEqBWrE7C7hYmtUk=

"""
