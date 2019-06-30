from oauth_builder import OauthBuilder


def test_authorization_header():
    """
    Use  known values from the twitter spec:
    https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request.html
    """
    oa = OauthBuilder(
        "xvz1evFS4wEEPTGEFPHBog",
        "no consumer secret",
        "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
        "no access key secret",
        {"no request": "params"},
    )
    oa._oauth_dict["oauth_nonce"] = "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg"
    oa._oauth_dict["oauth_timestamp"] = "1318622958"
    oa._oauth_dict["oauth_signature"] = "tnnArxj06cWHq44gCs1OSKk/jLY="
    s = oa.authorization_header()
    assert (
        s
        == 'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1318622958", oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", oauth_version="1.0"'
    )
