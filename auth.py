import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CREDENTIALS_FILE = "resources/client_secrets.json"
TOKEN_FILE = "token.pickle"

def get_authenticated_service():
    """
    Authenticate with YouTube API.
    In GitHub Actions, uses YOUTUBE_CREDENTIALS_JSON secret.
    Locally, uses OAuth flow with saved token.
    """
    try:
        credentials = None
        
        # First, try to load from environment (GitHub Actions)
        if os.getenv("YOUTUBE_CREDENTIALS_JSON"):
            logging.info("Loading credentials from GitHub Actions secret...")
            creds_json = json.loads(os.getenv("YOUTUBE_CREDENTIALS_JSON"))
            credentials = Credentials.from_authorized_user_info(creds_json, SCOPES)
            logging.info("Successfully authenticated with YouTube API from secret.")
            return build("youtube", "v3", credentials=credentials)
        
        # Otherwise, use local OAuth flow
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "rb") as token:
                credentials = pickle.load(token)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                logging.info("Refreshing expired credentials...")
                credentials.refresh(Request())
            else:
                logging.info("Starting OAuth flow for YouTube authentication...")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                # Only use run_local_server for local development
                credentials = flow.run_local_server(port=8080, prompt='consent', open_browser=True)
            
            # Save token for future use
            with open(TOKEN_FILE, "wb") as token:
                pickle.dump(credentials, token)
        
        logging.info("Successfully authenticated with YouTube API.")
        return build("youtube", "v3", credentials=credentials)
    
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        raise
