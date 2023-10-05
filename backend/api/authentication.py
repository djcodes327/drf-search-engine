from rest_framework.authentication import TokenAuthentication as BaseTokenAuth


class TokenAuthentication(BaseTokenAuth):
    # Bearer keyword will be used instead of token to pass in headers

    keyword = 'Token'
