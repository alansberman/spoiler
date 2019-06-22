from finder import *
from hidden import CLIENT_ID,CLIENT_SECRET
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Sender:

    def __init__(self):
        self.id = CLIENT_ID
        self.secret = CLIENT_SECRET
        self.Finder = None