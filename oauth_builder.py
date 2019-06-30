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
        sk = self._signing_key(consumer_secret, access_token_secret)
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

    def _signing_key(self, consumer_secret, access_token_secret):
        """
        The signing key is simply the percent encoded consumer secret, followed by an ampersand character ‘&’, followed by the percent encoded token secret.
        """
        return f"{self._percent_encode(consumer_secret)}&{self._percent_encode(access_token_secret)}"
