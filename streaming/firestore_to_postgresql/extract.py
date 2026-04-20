import os
from firebase_admin import firestore, initialize_app
from google.auth.credentials import AnonymousCredentials
from transform import transform
from load import load

def validate(doc: dict) -> bool:
    required = [
        "Country",
        "Quantity",
        "StockCode",
        "InvoiceDate",
        "uploaded_at",
        "CustomerID",
        "InvoiceNo",
        "UnitPrice",
        "Description",
        "TotalAmount"
    ]
    return all(field in doc for field in required)

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        change_type = change.type.name # ADDED, MODIFIED, DELETED
        doc = change.document.to_dict()

        if not validate(doc):
            print(f"  Document invalide skippé : {change.document.id}")
            continue

        record = transform(doc, change_type)
        load(record)



def start_extract_streaming(firestore_host: str, project_id: str):
    print(" - Extract Streaming Start")
    os.environ["FIRESTORE_EMULATOR_HOST"] = firestore_host
    os.environ["GCLOUD_PROJECT"] = project_id

    initialize_app(credential=AnonymousCredentials(), options={'projectId': project_id}) 
    client = firestore.client()

    col_ref = client.collection("orders")
    col_ref.on_snapshot(on_snapshot)

    