import json
import requests

# Configuration
CLIENT_ID = "610789219050-4t5sllktmufb7i56n3pklcbmbi9ut1jf.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080/"
AUTH_CODE = "4/0ATsMZqCZ2GjI8nl2Vuodf_qielUhZWl44phA0UuDdWqmpwi9J9fzj35Y3oQBBpJwikC3Hw"

# Exchange auth code for tokens
token_url = "https://oauth2.googleapis.com/token"
data = {
    "code": AUTH_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code"
}

response = requests.post(token_url, data=data)
tokens = response.json()

print("=" * 60)
print("YOUTUBE CREDENTIALS JSON FOR GITHUB SECRET")
print("=" * 60)
print(json.dumps(tokens, indent=2))
print("=" * 60)

# Save to file
with open("youtube_credentials.json", "w") as f:
    json.dump(tokens, f, indent=2)

print("\n✅ Credentials saved to youtube_credentials.json")
print("Copy the JSON above and add it as YOUTUBE_CREDENTIALS_JSON secret on GitHub!")
