"""Creates function that will create event from text inputs of information"""

from __future__ import print_function

import datetime
import os.path
import json
from pytz import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def event_create(start_date: list[int], end_date: list[int], title: str, location: str,
                 description: str, attendees: list[str]):
    """

    :param start_date: list of integers indicating the year, month, day, hour and minute of the
    start of the event in that order
    :param end_date: list of integers indicating the year, month, day, hour and minute of the end
    of the event in that order
    :param title: A string representing the title of the event
    :param location: A string representing the location of the event
    :param description: A string representing the a description of the event
    :param attendees: A list of the email addresses of the people attending the event
    """
    time_zone = timezone('EST')
    start_date = datetime.datetime(start_date[0], start_date[1], start_date[2], start_date[3],
                                   start_date[4], tzinfo=time_zone)
    end_date = datetime.datetime(end_date[0], end_date[1], end_date[2], end_date[3],
                                 end_date[4], tzinfo=time_zone)
    event_body_dict = {'summary': title, 'location': location, 'description': description,
                       'start': {'dateTime': start_date.isoformat()},
                       'end': {'dateTime': end_date.isoformat()}}
    attendees_body = []
    for attend in attendees:
        attendees_body.append({'email': attend})
    event_body_dict['attendees'] = attendees_body
    event_body = json.dumps(event_body_dict)
    event_object = json.loads(event_body)
    print(event_body)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=event_object).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('An error occurred: %s' % error)

# Test
# if __name__ == '__main__':
#     event_create([2022, 2, 5, 19, 6], [2022, 2, 5, 20, 0], "Event Creation",
#                  "Paris", "Hi", ["sjd3002@gmail.com"])
