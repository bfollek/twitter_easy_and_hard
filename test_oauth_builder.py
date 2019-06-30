from oauth_builder import OauthBuilder

# Use public values from the twitter spec to test:
# https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request.html
# https://developer.twitter.com/en/docs/basics/authentication/guides/creating-a-signature.html
HTTP_METHOD = "post"
BASE_URL = "https://api.twitter.com/1.1/statuses/update.json"
REQUEST_PARAMS = {
    "include_entities": "true",
    "status": "Hello Ladies + Gentlemen, a signed OAuth request!",
}
CONSUMER_KEY = "xvz1evFS4wEEPTGEFPHBog"
CONSUMER_SECRET = "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw"
ACCESS_TOKEN = "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb"
ACCESS_TOKEN_SECRET = "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
SIGNATURE = "tnnArxj06cWHq44gCs1OSKk/jLY="
NONCE = "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg"
TIMESTAMP = "1318622958"


def from_known_values():
    """
    Use  known values from the twitter spec:
    https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request.html
    """
    oa = OauthBuilder(
        HTTP_METHOD,
        BASE_URL,
        REQUEST_PARAMS,
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
    )
    oa._oauth_dict["oauth_nonce"] = NONCE
    oa._oauth_dict["oauth_timestamp"] = TIMESTAMP
    oa._oauth_dict["oauth_signature"] = SIGNATURE
    return oa


def test_authorization_header():
    oa = from_known_values()
    s = oa.authorization_header()
    assert (
        s
        == 'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1318622958", oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", oauth_version="1.0"'
    )


def test_sig_param_string():
    oa = from_known_values()
    s = oa._sig_param_string(REQUEST_PARAMS)
    assert (
        s
        == "include_entities=true&oauth_consumer_key=xvz1evFS4wEEPTGEFPHBog&oauth_nonce=kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1318622958&oauth_token=370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb&oauth_version=1.0&status=Hello%20Ladies%20%2B%20Gentlemen%2C%20a%20signed%20OAuth%20request%21"
    )


def test_sig_base_string():
    oa = from_known_values()
    sps = oa._sig_param_string(REQUEST_PARAMS)
    s = oa._sig_base_string(HTTP_METHOD, BASE_URL, sps)
    assert (
        s
        == "POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fupdate.json&include_entities%3Dtrue%26oauth_consumer_key%3Dxvz1evFS4wEEPTGEFPHBog%26oauth_nonce%3DkYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1318622958%26oauth_token%3D370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb%26oauth_version%3D1.0%26status%3DHello%2520Ladies%2520%252B%2520Gentlemen%252C%2520a%2520signed%2520OAuth%2520request%2521"
    )


def test_signing_key():
    oa = from_known_values()
    assert (
        oa._signing_key(CONSUMER_SECRET, ACCESS_TOKEN_SECRET)
        == "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw&LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
    )
