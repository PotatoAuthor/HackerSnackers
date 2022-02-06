

import datetime
import os.path
import random
from re import L
import LoginWindow
import gui
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gui import d

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

events15m = ['Screen break']
events30m =  ['discord call a friend', 'create a card or short video for someone far away', 'listen to some good music with a friend', 'make a cup of coffee/tea for someone', 'play a quick game of pickup basketball' , 'do a quick cardio workout', 'share you favorite tik tok']
events60m = ['play league of legends with your friends', 'go on a walk in the park with your friends', 'watching football with your friends', 'rock climbing with your friends', 'hit the gym and get gains with your gym bro', 'get a bubble tea with friends', 'watch an episode of sitcom with your bestie', 'go bowling with your bro', 'play a two person game like it takes 2', 'get a manicure with your girl/boy', 'drive around the city/country with the window down']
events120m = ['Ripley’s Aquarium with your friend', 'Edge Walk at CN with your friend', 'Go to the Art Galley of Ontario - (Free if you are between age of 14-25) with your friend'  , 'Dig around in Kensington market with your friend', 'take a hour long bath with your friend' , 'play a game of chess', 'write a short story with your friend', 'craft a complex meal with a special someone', 'attempt at a race of knitting']


# Brief:
#       Builds the schedule array, in which represents a 15 minute time window. If there is an event during
#       that window, the array contains a 1. Else, it contains a 0. Index 0 is the NEXT 15 minute timeslot from exectution.
#       i.e, if execution occurs at 11:54, 12:00-12:15 is the first index
#
# Parameters:
#           cals_to_check is an array of calendar names that the user wishes to read from
#           service is the object used to make calendar api calls
#           calendars_dict maps calendar names to their ids
#
# Returns: the schedule array
def get_free_time(cals_to_check, service, calendars_dict, max_scan_time_days):
        #fixed size array filled with 0s, which has the number of 15 minute time blocks in max_scan_time_days
        # minus one since the first bucket starts at the NEXT quarter hour
        schedule_array = [0]*(max_scan_time_days*96-1) 
        
        # gets current timestamp
        now = str(datetime.datetime.now(datetime.timezone.utc).isoformat()[:-6] + 'Z')  # 'Z' indicates UTC time
        # gets timestamp of the end of the serach range (in UTC)
        max_search_timestamp = str((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = max_scan_time_days, minutes = 15)).isoformat()[:-6] + 'Z')

        # this convoluted line of code finds the exact timestamp of the next quarter of an hour[LOCAL TIME]
        first_bucket_time = (datetime.datetime.now() + datetime.timedelta(minutes = 15-(datetime.datetime.now().minute % 15))).replace(microsecond=0, second = 0)

        # loop through each calendar that was selected
        for calendarName in cals_to_check:
            calId=calendars_dict[calendarName]

            # use page iteration to loop over all events between 2 time points. At the earliest, they must already be in progress at execution
            # At the latest, they must start before max_search_timestamp
            page_token = None
            while True:
                events = service.events().list(calendarId=calId, timeMin=now,
                                              timeMax=max_search_timestamp, singleEvents=True).execute()
                for event in events['items']:
                    # find the difference between the end time and the first bucket in the array
                    end_time = datetime.datetime.strptime(event['end']['dateTime'].replace('T', ' ')[:-6], '%Y-%m-%d %H:%M:%S') # [LOCAL TIME]
                    timediff = end_time - first_bucket_time # result is a timedelta object
                    minutesOffset = timediff.days*1440 + timediff.seconds//60
                    # index event_ending_index is the last index in the array which should be set to 'occupied'
                    event_ending_index = int(minutesOffset/15 -1)

                    # find the difference between the start time and the first bucket in the array
                    start_time = datetime.datetime.strptime(event['start']['dateTime'].replace('T', ' ')[:-6], '%Y-%m-%d %H:%M:%S') # [LOCAL TIME]
                    timediff = start_time - first_bucket_time # result is a timedelta object
                    minutesOffset = timediff.days*1440 + timediff.seconds//60
                    event_start_index = int(minutesOffset/15)

                    # fill the schedule array with 1's when the event is taking place
                    if (event_ending_index >= 0):
                        schedule_array[max(0, event_start_index):event_ending_index] = [1]*(event_ending_index-max(0, event_start_index)+1)
                        
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
        # use this to make python have a fixed length array
        return schedule_array[0:max_scan_time_days*96-1]

# taken from Google Calendar API quickstart guide, https://developers.google.com/calendar/api/quickstart/python
def authenticate():
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
    return creds

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

def main():
    LoginWindow.main()
    creds = authenticate()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Build a dictionary of calendars and their ids
        # calendars_dict will hold kv pairs, mapping calendar names to their ids
        calendars_dict = {}
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendars_dict[calendar_list_entry['summary']] = calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        
        # ask the user to check boxes indicating which calendars to analyze
        cals_to_check = gui.main(calendars_dict)

        # the max time to look at in days, this determines how far out calendar suggestrions will be made
        max_scan_time_days = 3
        free_time_array = get_free_time(cals_to_check, service, calendars_dict, max_scan_time_days)
        print (free_time_array)

        # call Ronit's function to get run lengths
        # which returns start time, end time, and run length (in terms of buckets)

        for data in run_lengths:
            start_datetimeobj, end_datetimeobj, runlen = data
            chosen_event = None
            if runlen >= 8:
                chosen_event = random.choice(events120m)
            elif runlen >= 4:
                chosen_event = random.choice(events60m)
            elif runlen >= 2:
                chosen_event = random.choice(events30m)
            elif runlen == 1:
                chosen_event = random.choice(events15m)
            start_date = [start_datetimeobj.year, start_datetimeobj.month, start_datetimeobj.day, start_datetimeobj.hour, start_datetimeobj.minute]
            end_date = [end_datetimeobj.year, end_datetimeobj.month, end_datetimeobj.day, end_datetimeobj.hour, end_datetimeobj.minute]
            event_create(start_date=start_date, end_date=end_date, title=chosen_event, location=None, description=None, attendees=None)
            print(chosen_event)
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()