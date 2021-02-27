import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials(client_secret_file='client_secret.json'):
    """
    Get credentials and store it in project folder for future using.
    Watch https://www.youtube.com/watch?v=vQQEaSnQ_bs for obtain client_secret.json
    :param client_secret_file: json file with user OAuth credentials
    :return: credentials for interact with YouTube API
    """
    credentials = None
    if os.path.exists('token.pickle'):
        print('Loading credentials from file...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing access token...')
            credentials.refresh(Request())
        else:
            print('Fetching new token...')
            # DOC -> https://developers.google.com/youtube/v3/guides/auth/installed-apps
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=client_secret_file, scopes=[
                'https://www.googleapis.com/auth/youtube',
                'https://www.googleapis.com/auth/youtube.channel-memberships.creator',
                'https://www.googleapis.com/auth/youtube.force-ssl',
                'https://www.googleapis.com/auth/youtube.readonly',
                # 'https://www.googleapis.com/auth/youtube.upload',
                # 'https://www.googleapis.com/auth/youtubepartner',
                # 'https://www.googleapis.com/auth/youtubepartner-channel-audit',
            ])
            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials
            with open('token.pickle', 'wb') as f:
                print('Saving credentials for future use...')
                pickle.dump(credentials, f)

    return credentials
