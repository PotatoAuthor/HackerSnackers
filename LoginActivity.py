#!/usr/bin/env python

"""
https://gist.github.com/clarketm/dc5d5be390e3f811a2dd7f5e8c5728ba
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

from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.file import Storage
from oauth2client.tools import run_flow

SCOPE = 'https://www.googleapis.com/auth/calendar.readonly'


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
    o_stdout, o_file = disable_stout()

    flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPE)

    storage = Storage('token.json')
    credentials = run_flow(flow, storage)
    enable_stout(o_stdout, o_file)

    print("access_token: %s" % credentials.access_token)
