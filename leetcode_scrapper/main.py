from pytz import timezone
from datetime import datetime
from bs4 import BeautifulSoup
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
import os
import pickle
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", scopes=scopes)
if os.path.exists('token.pkl'):
    credentials = pickle.load(open("token.pkl", "rb"))
else:
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
idc = '9ahl9nu5h247gso88oh15qkp64@group.calendar.google.com'
events_result = service.events().list(calendarId=idc).execute()
events = events_result.get('items', [])
url = requests.get('https://kontests.net/api/v1/leet_code').json()

new_event = {
    'summary': 'leetcode contest',
    'start': {
        'dateTime': '2015-05-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2015-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'reminders': {
        'useDefault': True,
    },
    'source': {
        'url': 'https://leetcode.com/contest/weekly-contest-236',
        'title': 'Weekly Contest 236'
    }
}
for contest in url:
    new_event['start']['dateTime'] = contest['start_time']
    new_event['end']['dateTime'] = contest['end_time']
    new_event['source']['url'] = contest['url']
    new_event['source']['title'] = contest['name']
    new_event['summary'] = 'Leetcode ' + contest['name']
    flag = 0
    for existing_event in events:
        if(new_event['summary'] == existing_event['summary']):
            flag = 1
            break
    if(flag == 0):
        service.events().insert(calendarId= idc, body = new_event).execute()
