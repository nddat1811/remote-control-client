from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email
import time
from bs4 import BeautifulSoup
import uuid
from email.mime.text import MIMEText
from requests import HTTPError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://mail.google.com/"
]

def authorization():
    creds = ""
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            path = os.path.abspath('credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next runserver\credentials.json
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
def send_mail(package):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    service = build('gmail', 'v1', credentials=creds)
    message_body = '{}'.format(package)  # sử dụng phương thức format() để thêm giá trị vào nội dung email
    message = MIMEText(message_body)

    message['to'] = 'testpython18mmt@gmail.com'
    message['subject'] = 'client'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
    message = None
def read_mail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        # query list message with subject client and not read
        results = service.users().messages().list(userId='me', q='is:unread subject:server').execute()
        # results = service.users().messages().list(userId='me').execute()
        mes = results.get('messages', [])
        if not mes:
            print("No letter find out")
            return "no"
        else:
            for m in mes:
                 # Call the Gmail v1 API, retrieve message data.
                message = service.users().messages().get(userId='me', id=m['id'], format="raw").execute()

                res = get_info_message(message)

                """
                Đánh dấu thư là đã đọc
                """
                # Mark read letter from gmail
                mark_as_read(service, m)
                return res

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
def get_info_message(message):
    # Parse the raw message.
    mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(message['raw']))
    t = ""
    message_main_type = mime_msg.get_content_maintype()
    if message_main_type == 'multipart':
        for part in mime_msg.get_payload():
            if part.get_content_maintype() == 'text':
                t = part.get_payload()
    elif message_main_type == 'text':
        t = mime_msg.get_payload()
    print("\n",t)
    return t


def mark_as_read(service, m):
    service.users().messages().modify(userId='me', id=m['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    return
def split_messages(letter):
    tmp = letter.split(":")
    cmd = tmp[0]
    data = tmp[1]
    return cmd, data

def get_mail_with_attachment(path):
    creds = None

    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        # query list message with subject client and not read
        results = service.users().messages().list(userId='me', q='is:unread subject:server').execute()
        # results = service.users().messages().list(userId='me').execute()
        mes = results.get('messages', [])
        mes.reverse() #oldest
        if not mes:
            print("No letter find out")
            return "no"
        else:
            for m in mes:
                message = service.users().messages().get(userId='me', id=m['id'], format="raw").execute()

                res = get_info_message(message)
                if "LIVESCREEN" in res:
                    message = service.users().messages().get(userId='me', id=m['id']).execute()
                    for part in message['payload']['parts']:
                        if(part['filename'] and part['body'] and part['body']['attachmentId']):
                            attachment = service.users().messages().attachments().get(id=part['body']['attachmentId'], userId='me', messageId=m['id']).execute()

                            file_data = base64.urlsafe_b64decode(attachment['data'].encode('utf-8'))
                            current_path = os.path.dirname(__file__)
                            desPath = f"{current_path}/livescreen/{part['filename']}"
                            
                            f = open(desPath, 'wb')
                            f.write(file_data)
                            f.close()
                    #xoá thư
                    service.users().messages().delete(userId='me', id=m['id']).execute()
                return res

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def clear_all_msg():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        # query list message with subject client and not read
        results = service.users().messages().list(userId='me').execute()
        # results = service.users().messages().list(userId='me').execute()
        mes = results.get('messages', [])
        if not mes:
            print("No letter find out to delete")
        else:
            for m in mes:
                service.users().messages().delete(userId='me', id=m['id']).execute()
            print("delete all")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
# https://skillshats.com/blogs/send-and-read-emails-with-gmail-api/ link có hết
#https://www.youtube.com/watch?v=HNtPG5ltFf8
#https://developers.google.com/gmail/api/guides/labels