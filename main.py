

import datetime
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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

def main():
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
        # ask the user to check boxes indicating which calendars to analyze.

        cals_to_check = ['golem8gamer@gmail.com', 'Holidays in Canada', 'broland']
        max_scan_time_days = 3
        free_time_array = get_free_time(cals_to_check, service, calendars_dict, max_scan_time_days)
        print (free_time_array)


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()