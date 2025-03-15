import json
import os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """Initialize Firebase using credentials from an environment variable."""
    firebase_json = os.getenv("FIREBASE_CREDENTIALS")

    if firebase_json:
        firebase_creds = json.loads(firebase_json)  # Convert string to dict
        cred = credentials.Certificate(firebase_creds)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
    else:
        raise ValueError("🔥 Firebase credentials not found! Set FIREBASE_CREDENTIALS environment variable.")
