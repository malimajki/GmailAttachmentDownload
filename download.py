import os
import base64
import json
import re
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SENDER_EMAIL = 'expale@gmail.com'
DOWNLOAD_DIR = 'attachments'

def authenticate_gmail():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = service_account.Credentials.from_authorized_user_file('token.json', SCOPES)
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

def search_emails(service, query):
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_attachments(service, message_id, prefix=""):
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        parts = message.get('payload', {}).get('parts', [])
        for part in parts:
            if part.get('filename'):
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body'].get('attachmentId')
                    att = service.users().messages().attachments().get(userId='me', messageId=message_id, id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = os.path.join(DOWNLOAD_DIR, prefix + part['filename'])

                with open(path, 'wb') as f:
                    f.write(file_data)
                print(f'Attachment {part["filename"]} saved to {path}')
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Create the directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    query = f'from:{SENDER_EMAIL} has:attachment'
    messages = search_emails(service, query)
    if not messages:
        print('No messages found.')
        return

    for message in messages:
        get_attachments(service, message['id'])

if __name__ == '__main__':
    main()
