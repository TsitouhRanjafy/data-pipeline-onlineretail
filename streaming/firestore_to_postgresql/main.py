from extract import start_extract_streaming
from fastapi import FastAPI
from contextlib import asynccontextmanager
from psycopg2 import pool
from load import DB_CONFIG
import os
from firebase_admin import initialize_app, firestore
from google.auth.credentials import AnonymousCredentials

FIRESTORE_EMULATOR_HOST = "192.168.1.100:8082"
PROJECT_ID = "demo-event-app"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # démarre au lancement du serveur
    start_extract_streaming(FIRESTORE_EMULATOR_HOST, PROJECT_ID)
    
    yield  # serveur tourne ici
    
    # cleanup à l'arrêt du serveur
    print(" Pipeline arrêté")

app = FastAPI(lifespan=lifespan)

@app.get("/status")
def read_root():
    os.environ["FIRESTORE_EMULATOR_HOST"] = FIRESTORE_EMULATOR_HOST
    os.environ["GCLOUD_PROJECT"] = PROJECT_ID

    initialize_app(credential=AnonymousCredentials(), options={'projectId': PROJECT_ID}) 
    client = firestore.client()
    return {"pipeline_status": "running"}