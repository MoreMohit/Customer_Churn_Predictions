import os
import json
import firebase_admin
from firebase_admin import credentials

# 🔥 Load Firebase credentials from environment variable
firebase_json_base64 = os.getenv("FIREBASE_CREDENTIALS")

if firebase_json_base64:
    firebase_json = json.loads(firebase_json_base64)  # Decode Base64 to JSON
    cred = credentials.Certificate(firebase_json)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
else:
    raise ValueError("🔥 Firebase credentials not found! Set the FIREBASE_CREDENTIALS environment variable.")
