#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httplib2

import os
import shutil
import subprocess
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = os.environ.get('CLIENT_SECRET_SHEET')
APPLICATION_NAME = 'support'


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
    credential_file_name = os.environ.get('CREDENTIAL_FILE_SHEET')
    credential_path = os.path.join(credential_dir, credential_file_name)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_pycon_urls_from_sheet():
    addr_set = []

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # https://developers.google.com/sheets/guides/concepts
    spreadsheetId = os.environ.get('SPREAD_SHEET_ID')
    rangeName = 'Sheet1!K2:L'
    print('[INFO]get value start')
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            addr_set.append(row[0])
    return addr_set


def download_by_youtubedl(pycon_urls):
    pycon_subtitle = 'PyconSubtitle'
    if os.path.exists(pycon_subtitle):
        shutil.rmtree(pycon_subtitle)
    os.makedirs(pycon_subtitle)
    os.chdir(pycon_subtitle)

    for idx, url in enumerate(pycon_urls):
        command = 'youtube-dl --write-sub --sub-lang en --sub-format vtt --skip-download %s' % url
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode != 0:
            print('{}[ERR ] {}'.format(idx, url))
        else:
            print('{}[INFO] {}'.format(idx, url))


def main():

    pycon_urls = get_pycon_urls_from_sheet()
    # print(pycon_addresses)
    download_by_youtubedl(pycon_urls)


if __name__ == '__main__':
    main()
