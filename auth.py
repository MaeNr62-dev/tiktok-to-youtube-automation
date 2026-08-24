import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import logging

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CREDENTIALS_FILE = "resources/client_secrets.json"

def get_authenticated_service():
    try:
        credentials = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                # Pour GitHub Actions (serveur sans interface), utilise run_console()
                # Pour développement local avec interface, on peut utiliser run_local_server()
                try:
                    credentials = flow.run_console()
                except Exception:
                    # Fallback si run_console() ne fonctionne pas
                    credentials = flow.run_local_server(port=8080, prompt='consent', open_browser=False)
                with open("token.pickle", "wb") as token:
                    pickle.dump(credentials, token)
        logging.info("Successfully authenticated with YouTube API.")
        return build("youtube", "v3", credentials=credentials)
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        raise
