import os
import pandas as pd
import firebase_admin
from firebase_admin import firestore, delete_app
import datetime
from google.auth.credentials import AnonymousCredentials

os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8082"
os.environ["GCLOUD_PROJECT"] = "demo-event-app"

firebase_admin.initialize_app(credential=AnonymousCredentials(), options={'projectId': 'demo-event-app'}) 

client = firestore.client()

def load_batch_to_firestore(df: pd.DataFrame, collection_name: str = "orders") -> int:
    """
    Charge les données dans Firestore Emulator en utilisant des batches (limite 500).
    """
    
    batch = client.batch()
    count = 0
    total = 0
    
    for _, row in df.iterrows():
        doc_data = row.to_dict()
        
        doc_data['uploaded_at'] = datetime.datetime.now()
        
        doc_ref = client.collection(collection_name).document()  
        batch.set(doc_ref, doc_data)
        
        count += 1
        total += 1
        
        if count >= 499:
            batch.commit()
            print(f"   → Batch de {count} documents commité, total {total}")
            batch = client.batch()
            count = 0
    
    if count > 0:
        batch.commit()

    return total


