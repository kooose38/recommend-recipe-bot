import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
import datetime
import uuid 
import os 

cred = credentials.Certificate(f"firebase/{os.getenv("FIREBASE_KEY")}")
firebase_admin.initialize_app(cred)

db = firestore.client()

def request_post_user(kwd):
    try:
        now = str(datetime.datetime.now())
        uid = str(uuid.uuid4())
        ref = db.collection(u"users").document(uid)
        ref.set({
            "uid": uid, 
            "created_at": now, 
            "keyword": kwd 
        })

        print("[INFO] success add database.")
    except Exception as e:
        print(f"[ERROR] {print(e)}")
