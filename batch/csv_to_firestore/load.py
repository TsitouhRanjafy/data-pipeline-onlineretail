import os
import pandas as pd
import firebase_admin
from firebase_admin import firestore, delete_app
import datetime
from google.auth.credentials import AnonymousCredentials


def load_batch_to_firestore(df: pd.DataFrame, firestore_client, collection_name: str = "orders") -> int:
    """
    Charge les données dans Firestore Emulator en utilisant des batches (limite 500).
    """
    
    batch = firestore_client.batch()
    count = 0
    total = 0
    
    for _, row in df.iterrows():
        doc_data = row.to_dict()
        
        doc_data['uploaded_at'] = datetime.datetime.now()
        
        doc_ref = firestore_client.collection(collection_name).document()  
        batch.set(doc_ref, doc_data)
        
        count += 1
        total += 1
        
        if count >= 499:
            batch.commit()
            print(f"   → Batch de {count} documents commité, total {total}")
            batch = firestore_client.batch()
            count = 0
    
    if count > 0:
        batch.commit()

    return total

def load(df: pd.DataFrame, firestore_host: str, project_id: str):
    os.environ["FIRESTORE_EMULATOR_HOST"] = firestore_host
    os.environ["GCLOUD_PROJECT"] = project_id

    app = firebase_admin.initialize_app(credential=AnonymousCredentials(), options={'projectId': project_id}) 
    client = firestore.client()

    print(f"  Load to firestore START, total row: {len(df)} ")
    total_loaded = load_batch_to_firestore(df, client)
    print(f"✅ {total_loaded} row loaded")

    # firebase_admin.delete_app(app)