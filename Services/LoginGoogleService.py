import json
from flask import Flask, redirect, request, session, url_for, jsonify
from flask_login import login_user
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from Utilities.RamdomCode import ramdomCode
import Services.DaoService as daoService
from googleapiclient.discovery import build
import os

from Models.AccountModel import AccountModel

CLIENT_ID = '1011629016018-58pau0049l1ubhpvogcjllun8d9tom03.apps.googleusercontent.com'
CLIENT_SECRET = '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'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
REDIRECT_URI = 'http://127.0.0.1:5000/OnlineClass/callback'
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile']


def login():
    flow = Flow.from_client_secrets_file(
        'Services/client_google.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return authorization_url


def callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        'Services/client_google.json',
        scopes=None,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    if creds.refresh_token:
        refresh_token = creds.refresh_token
        print("Refresh token:", refresh_token)
    else:
        print("Không nhận được refresh token từ Google.")
    session['creds'] = creds.to_json()
    user = inforUser(creds)
    print("a:", session['creds'])
    findAccount = daoService.findById(AccountModel, user['email'])
    if findAccount is None:
        folder = createFolder(creds, "ClassOnline")
        account = AccountModel(user['email'], ramdomCode(), user['name'], user['picture'], idFolder=folder)
        daoService.create(account)
        login_user(account)
    else:
        login_user(findAccount)
    return redirect('http://127.0.0.1:5000/OnlineClass/home')


def createFolder(creds, nameFolder, *args):
    file_metadata = {
        "name": nameFolder,
        "mimeType": "application/vnd.google-apps.folder"
    }
    # Kiểm tra xem có dữ liệu trong args không
    if args:
        parent_folder_id = args[0]
        file_metadata['parents'] = [parent_folder_id]

    drive_service = build("drive", "v3", credentials=creds)
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    return folder.get("id")

def createFile(idFolder):
    pass


def inforUser(creds):
    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()
    return user_info
