import os
import json
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """
    Authenticate with YouTube API using stored credentials from environment.
    """
    try:
        credentials = None
        
        # Load credentials from environment variable (GitHub Actions)
        if os.getenv("YOUTUBE_CREDENTIALS_JSON"):
            logging.info("Loading credentials from YOUTUBE_CREDENTIALS_JSON...")
            try:
                creds_json = json.loads(os.getenv("YOUTUBE_CREDENTIALS_JSON"))
                # Create credentials from the token info
                credentials = Credentials(
                    token=creds_json.get("access_token"),
                    refresh_token=creds_json.get("refresh_token"),
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=creds_json.get("client_id"),
                    client_secret=creds_json.get("client_secret"),
                    scopes=SCOPES
                )
                logging.info("Successfully loaded credentials from environment.")
                return build("youtube", "v3", credentials=credentials)
            except Exception as e:
                logging.error(f"Failed to load credentials from environment: {e}")
                raise
        else:
            logging.error("YOUTUBE_CREDENTIALS_JSON environment variable not set!")
            raise ValueError("YOUTUBE_CREDENTIALS_JSON environment variable is required")
    
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        raise
