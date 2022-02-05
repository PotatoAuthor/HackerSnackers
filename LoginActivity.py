#!/usr/bin/env python

"""
This script will attempt to open your webbrowser,
perform OAuth 2.0 authentication and print your access token.
To install dependencies from PyPI:
  $ pip install oauth2client
Then run this script:
  $ python get_oauth2_token.py
This is a combination of snippets from:
  https://developers.google.com/api-client-library/python/guide/aaa_oauth
  https://gist.github.com/burnash/6771295
"""

import os
import sys

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run_flow


def return_token():
    return get_oauth2_token()


def disable_stout():
    o_stdout = sys.stdout
    o_file = open(os.devnull, 'w')
    sys.stdout = o_file
    return o_stdout, o_file


def enable_stout(o_stdout, o_file):
    o_file.close()
    sys.stdout = o_stdout


def get_oauth2_token():
    CLIENT_ID = "581786658708-elflankerquo1a6vsckabbhn25hclla0.apps.googleusercontent.com"
    CLIENT_SECRET = "3f6NggMbPtrmIBpgx-MK2xXK"
    SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
    REDIRECT_URI = '<Redirect URI from Google API Console>'

    o_stdout, o_file = disable_stout()

    flow = OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI)

    storage = Storage('creds.data')
    credentials = run_flow(flow, storage)
    enable_stout(o_stdout, o_file)

    print("access_token: %s" % credentials.access_token)


if __name__ == '__main__':
    return_token()

