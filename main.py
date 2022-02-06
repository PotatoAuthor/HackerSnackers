import datetime
import os.path
import random
from re import L
import LoginWindow
import gui
import json
import time
import freeTimes
from pytz import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gui import d

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Stores event ideas based on how much time is free
events15m = ['Screen break']
events30m = ['discord call a friend', 'create a card or short video for someone far away',
             'listen to some good music with a friend', 'make a cup of coffee/tea for someone',
             'play a quick game of pickup basketball', 'do a quick cardio workout',
             'share you favorite tik tok']
events60m = ['play league of legends with your friends',
             'go on a walk in the park with your friends', 'watching football with your friends',
             'rock climbing with your friends', 'hit the gym and get gains with your gym bro',
             'get a bubble tea with friends', 'watch an episode of sitcom with your bestie',
             'go bowling with your bro', 'play a two person game like it takes 2',
             'get a manicure with your girl/boy',
             'drive around the city/country with the window down']
events120m = ['Ripley’s Aquarium with your friend', 'Edge Walk at CN with your friend',
              'Go to the Art Galley of Ontario - (Free if you are between age of 14-25) with your'
              ' friend',
              'Dig around in Kensington market with your friend', 'play a game of chess',
              'write a short story with your friend', 'craft a complex meal with a special someone',
              'attempt at a race of knitting']


def get_free_time(cals_to_check, service, calendars_dict, max_scan_time_days: int) -> list[int]:
    """
    Returns a fixed size list filled with 0s and 1s, which has the number of 15 minute time blocks
    in max_scan_time_days minus one since the first bucket starts at the NEXT quarter hour.
    Index 0 is the NEXT 15 minute timeslot from execution. i.e, if execution occurs at 11:54,
    12:00-12:15 is the first index.

    For each time block, if there is an event during that window, the array contains a 1.
    Else, it contains a 0.

    :param cals_to_check: an array of calendar names that the user wishes to read from
    :param service: service is the object used to make calendar api calls
    :param calendars_dict: calendars_dict maps calendar names to their ids
    :param max_scan_time_days: The number of days you scan for free time
    :return: A list of 1's and 0's, where 0's represent free time and 1 busy
    """
    schedule_array = [0] * (max_scan_time_days * 96 - 1)

    # gets current timestamp
    now = str(datetime.datetime.now(datetime.timezone.utc).isoformat()[
              :-6] + 'Z')  # 'Z' indicates UTC time
    # gets timestamp of the end of the serach range (in UTC)
    max_search_timestamp = str((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=max_scan_time_days, minutes=15)).isoformat()[:-6] + 'Z')

    # this convoluted line of code finds the exact timestamp of the next quarter of
    # an hour[LOCAL TIME]
    first_bucket_time = (datetime.datetime.now() + datetime.timedelta(
        minutes=15 - (datetime.datetime.now().minute % 15))).replace(microsecond=0, second=0)

    # loop through each calendar that was selected
    for calendarName in cals_to_check:
        cal_id = calendars_dict[calendarName]

        # use page iteration to loop over all events between 2 time points. At the earliest,
        # they must already be in progress at execution
        # At the latest, they must start before max_search_timestamp
        page_token = None
        while True:
            events = service.events().list(calendarId=cal_id, timeMin=now,
                                           timeMax=max_search_timestamp,
                                           singleEvents=True).execute()
            for event in events['items']:
                # find the difference between the end time and the first bucket in the array
                end_time = datetime.datetime.strptime(
                    event['end']['dateTime'].replace('T', ' ')[:-6],
                    '%Y-%m-%d %H:%M:%S')  # [LOCAL TIME]
                timediff = end_time - first_bucket_time  # result is a timedelta object
                minutes_offset = timediff.days * 1440 + timediff.seconds // 60
                # index event_ending_index is the last index in the array which should be set
                # to 'occupied'
                event_ending_index = int(minutes_offset / 15 - 1)

                # find the difference between the start time and the first bucket in the array
                start_time = datetime.datetime.strptime(
                    event['start']['dateTime'].replace('T', ' ')[:-6],
                    '%Y-%m-%d %H:%M:%S')  # [LOCAL TIME]
                timediff = start_time - first_bucket_time  # result is a timedelta object
                minutes_offset = timediff.days * 1440 + timediff.seconds // 60
                event_start_index = int(minutes_offset / 15)

                # fill the schedule array with 1's when the event is taking place
                if event_ending_index >= 0:
                    schedule_array[max(0, event_start_index):event_ending_index] = [1] * (
                            event_ending_index - max(0, event_start_index) + 1)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    # time_loop is a datetime object used to loop through all 15 minute blocks we check in
    # schedule array
    time_loop = (datetime.datetime.now() + datetime.timedelta(
        minutes=15 - (datetime.datetime.now().minute % 15))).replace(microsecond=0, second=0)
    index = 0  # The index keeps track of which 15 minute block we are in
    while index < (max_scan_time_days * 96 - 1):
        morning_bound_start = time_loop.replace(hour=8, minute=0)
        night_bound_start = time_loop.replace(hour=22, minute=0)
        # If the time block we are in falls within night hours , after 10 pm or before 8 am, we set
        # it to busy
        if time_loop > night_bound_start or time_loop < morning_bound_start:
            schedule_array[index] = 1
        index += 1
        time_loop = time_loop + datetime.timedelta(minutes=15)

    # use this to make python have a fixed length array
    return schedule_array[0:max_scan_time_days * 96 - 1]


# taken from
def authenticate():
    """
    This method is taken from Google Calendar API quickstart guide,
    https://developers.google.com/calendar/api/quickstart/python
    and is used to verify the credentials of the user
    :return: credentials for using Google Calendar API
    """
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
                 description: str, attendees: list[str], service, calendars_dict):
    """
    This method takes in information to create an event in Google Calendar, and performs an API
    call to do so.

    :param start_date: list of integers indicating the year, month, day, hour and minute of the
    start of the event in that order
    :param end_date: list of integers indicating the year, month, day, hour and minute of the end
    of the event in that order
    :param title: A string representing the title of the event
    :param location: A string representing the location of the event
    :param description: A string representing the a description of the event
    :param attendees: A list of the email addresses of the people attending the event
    :param service: service is the object used to make calendar api calls
    :param calendars_dict: calendars_dict maps calendar names to their ids
    """
    # Sets the timezone
    time_zone = timezone('EST')
    # Assemble datetime objects for the starting and ending time of event
    start_date = datetime.datetime(start_date[0], start_date[1], start_date[2], start_date[3],
                                   start_date[4], tzinfo=time_zone)
    end_date = datetime.datetime(end_date[0], end_date[1], end_date[2], end_date[3],
                                 end_date[4], tzinfo=time_zone)
    # Assembles the dictionary containing all info of event
    event_body_dict = {'summary': title, 'location': location, 'description': description,
                       'start': {'dateTime': start_date.isoformat()},
                       'end': {'dateTime': end_date.isoformat()}}
    # We add the emails of attendees to event_body_dict
    attendees_body = []
    for attend in attendees:
        attendees_body.append({'email': attend})
    event_body_dict['attendees'] = attendees_body
    # We then create a Json string from our dictionary, then cast it to a Json object
    event_body = json.dumps(event_body_dict)
    event_object = json.loads(event_body)

    # Now we access the calendar to create the object
    try:
        service.events().insert(calendarId=calendars_dict['Amitee Suggestions'],
                                body=event_object).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)


def main() -> None:
    """
    The function organizes opening our application, and the actual process of finding empty time
    blocks, and creating events to do something in them
    :return: function returns nothing
    """
    # We open the login window and start authentication of credentials to access Google Calendar
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
        # create calendar for suggestions if it doesnt exist already
        if not 'Amitee Suggestions' in calendars_dict.keys():
            calendar = {
                'summary': 'Amitee Suggestions',
            }
            amitee_calendar = service.calendars().insert(body=calendar).execute()
            calendars_dict['Amitee Suggestions'] = amitee_calendar['id']

        # ask the user to check boxes indicating which calendars to analyze
        cals_to_check = gui.main(calendars_dict)

        # the max time to look at in days, this determines how far out calendar suggestions
        # will be made
        max_scan_time_days = 3
        # Gets the blocks when the person is free and chooses a random social event to fill that
        # gap
        free_time_array = get_free_time(cals_to_check, service, calendars_dict, max_scan_time_days)
        for data in freeTimes.free_times(free_time_array):
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
            # We then create that social event in Google Calendar
            start_date = [start_datetimeobj.year, start_datetimeobj.month, start_datetimeobj.day,
                          start_datetimeobj.hour, start_datetimeobj.minute]
            end_date = [end_datetimeobj.year, end_datetimeobj.month, end_datetimeobj.day,
                        end_datetimeobj.hour, end_datetimeobj.minute]

            event_create(start_date=start_date, end_date=end_date, title=chosen_event,
                         location='', description='', attendees=[], service=service,
                         calendars_dict=calendars_dict)
            # print(chosen_event)
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
