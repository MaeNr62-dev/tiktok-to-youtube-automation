#!/usr/bin/env python3
"""
Script to convert Google OAuth authorization code to access token.
Run this once to generate YOUTUBE_CREDENTIALS_JSON for GitHub secret.
"""

import requests
import json
import sys

# Your OAuth credentials from Google Cloud Console
CLIENT_ID = "610789219050-4t5sllktmufb7i56n3pklcbmbi9ut1jf.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080/"

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access and refresh tokens."""
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    print(f"Exchanging authorization code for tokens...")
    response = requests.post(token_url, data=data)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    tokens = response.json()
    return tokens

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_token.py <authorization_code>")
        print("\nExample:")
        print("python3 get_token.py '4/0ATsMZqBnPTBKf1KQaeQcUgyTOaTP46KQcJ-Lg6tlADVtnaTObKzqWTydWOOjDR7CuPGZEw'")
        sys.exit(1)
    
    auth_code = sys.argv[1]
    tokens = exchange_code_for_token(auth_code)
    
    if tokens:
        print("\n" + "="*70)
        print("✅ SUCCESS! Copy this JSON and add it as YOUTUBE_CREDENTIALS_JSON secret:")
        print("="*70)
        print(json.dumps(tokens, indent=2))
        print("="*70)
        
        # Also save to file
        with open("youtube_token.json", "w") as f:
            json.dump(tokens, f, indent=2)
        print("\n✅ Saved to youtube_token.json")
    else:
        print("❌ Failed to get tokens")
        sys.exit(1)

if __name__ == "__main__":
    main()
