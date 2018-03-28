# -*- encoding: utf-8 -*-

import httplib2
import os
import pprint
import datetime
import dateutil.parser

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Get Calendar Information'

def get_credentials():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedir(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar_data.json')
    store = Storage(credential_path)
    credentials = store.get()

    if (not credentials) or credentials.invalid:
        # credentialsが取得できない　もしくは　credentialが不正のとき
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)

    return credentials


def get_schedule():
    res = []
    credentials = get_credentials()
    m_http = credentials.authorize(httplib2.Http())
    m_service = discovery.build('calendar', 'v3', http=m_http)

    #'Z' は UTC timeを示している
    current_time = datetime.datetime.utcnow().isoformat() + 'Z'
    print('直近の3個のイベントを取得します。')
    events_result = m_service.events().list(
        calendarId   = 'primary',
        timeMin      = current_time,
        maxResults   = 3,
        singleEvents = True,
        orderBy      = 'startTime'
        ).execute()
    events = events_result.get('items', [])

    if not events:
        print('直近のイベントが見つかりませんでした。')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date_data = "{0:%m月%d日 %H時%M分から}".format(dateutil.parser.parse(start))
        with open('date.txt', 'w') as data:
            data.write(pprint.pformat(event))
        print(date_data, event['summary'])
        res.append([date_data, event['summary']])
    return res


def create_schedule():
    eventTitle = "タイトル"
    eventSummary = "詳細"
    eventDateData = []