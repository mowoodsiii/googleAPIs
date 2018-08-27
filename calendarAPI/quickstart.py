from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

# calID='colorado.edu_4vko1g9ooke1ssloilp5ov3360@group.calendar.google.com'
calID='mawo4813@colorado.edu'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 100 events\n')
    eventsResult = service.events().list(
        calendarId=calID, timeMin=now, maxResults=50, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    appointmentIds=[]
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if(1):
        #if ("appointment" in event['summary'].lower()) or ("meet with" in event['summary'].lower()) or ("workshop" in event['summary'].lower()) or ("meeting" in event['summary'].lower()) or ("3d printer service" in event['summary'].lower()):
            appointmentIds.append(event['id'])
            if ("appointment" in event['summary'].lower() or "meet with" in event['summary'].lower() or "3d printer service" in event['summary'].lower()):
                event['colorId']='11' # bold red
                print('Appointment: ',event['summary'])
            elif ("workshop" in event['summary'].lower()):
                event['colorId']='3'  # lavender
                print('Workshop:    ',event['summary'])
            elif ("meeting" in event['summary'].lower()):
                event['colorId']='5'  # yellow
                print('Meeting:     ',event['summary'])
            elif ("arrives" not in event['summary'].lower() and "departs" not in event['summary'].lower() and "lunch" not in event['summary'].lower()):
                event['colorId']='9' # blue
                print('Other:       ',event['summary'])
            service.events().update(calendarId=calID, eventId=event['id'],body=event).execute()
    print("\nNumber of appointments found:",len(appointmentIds))

if __name__ == '__main__':
    main()
