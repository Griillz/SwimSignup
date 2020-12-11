from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import re
import base64

class EmailParser:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.modify']

    def get_value_chosen(self):
        expected_sender = 'anthonydeangelis7877@gmail.com'
        value_chosen = -1
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)


        threads = service.users().threads().list(userId='me').execute().get('threads', [])
        # print(threads)
        count = 0
        results = service.users().messages().list(userId='me',labelIds=['INBOX']).execute()
        messages = results.get('messages',[])
        count = 0
        limit = 5
        email_sender = ''
        if not messages:
            print("no messages")
        else:
            for  message in messages:
                if count < limit:
                    msg = service.users().messages().get(userId='me',id=message['id']).execute()
                    labels = msg['labelIds']
                    msgid = msg['id']
                    headers = msg['payload']['headers']
                    for item in headers:
                        if item['name'] == 'From':
                            sender = item['value']
                            senderlist = sender.split('<')
                            email_sender = senderlist[1][0:-1]
                            if email_sender == expected_sender:
                                if 'UNREAD' in labels:
                                    service.users().messages().modify(userId='me',id=msgid, body={'removeLabelIds': ['UNREAD']}).execute()
                                    part = msg['payload']['parts'][0]
                                    body = part['body']['data'] + '=='
                                    decoded = base64.b64decode(body)
                                    decoded_further = decoded.decode('utf-8')
                                    try:
                                        parsed_value = int(re.search(r'\d+', decoded_further).group())
                                        value_chosen = parsed_value
                                    except:
                                        print("no value found")
                                    if value_chosen != -1:
                                        return value_chosen
                    count+=1

        return 'none'

    # def signUpFailed(self):
    #     print("nah brother")

if __name__ == "__main__":
    testing = EmailParser()
    testing.get_value_chosen()