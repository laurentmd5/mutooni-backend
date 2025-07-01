import os
import firebase_admin
from firebase_admin import credentials

cred_path = os.getenv("FIREBASE_CREDENTIALS")
if cred_path and not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
