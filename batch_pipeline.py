import pandas as pd
from datetime import datetime, timedelta
from helpers import prepare_dates_for_firestore
from load_to_firestore_emulator import load_batch_to_firestore

def extract(filepath: str) -> pd.DataFrame:
    """Load raw orders from a daily export file."""
    """The CSV file not formated in UTF-8 (Pandas default extraction) but in ISO-8859-1"""
    df = pd.read_csv(filepath, encoding='ISO-8859-1', parse_dates=["InvoiceDate"])
    print("✅ Extracted")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy() 

    # Transforme to datetime python native les date
    df = prepare_dates_for_firestore(df)

    # Supprimer les Quantity > 0
    df = df[df["Quantity"] > 0].copy()

    # Supprimer les lignes sans CustomerID
    df = df.dropna(subset=["CustomerID"]) 

    # Ajouter colonne pour prix total
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    df['TotalAmount'] = df['TotalAmount'].round(2) 

    # Nettoyage des colonnes texte
    df['Description'] = df['Description'].str.strip()     # enlever espaces inutiles
    df['Country'] = df['Country'].str.strip()

    print(f"✅ Transformation terminée : {len(df):,} lignes après nettoyage")
    print(f"✅ Colonnes finales : {list(df.columns)}")
    return df

def load(df: pd.DataFrame, output_path: str) -> None:
    """Write the aggregated result to the warehouse (here, a CSV)."""
    df.to_csv(output_path, index=False)
    print(f"✅ Loaded {len(df)} rows to {output_path}")


def load_to_firestore(df: pd.DataFrame):
    print(f"  Load to firestore START, total row: {len(df)} ")
    total_loaded = load_batch_to_firestore(df)
    print(f"✅ {total_loaded} row loaded")




# Run the pipeline
def run():
    try:
        raw = extract("./data/OnlineRetail.csv")
        aggregated = transform(raw)
        load(aggregated, f"warehouse/daily_online_retail_{datetime.now().date()}.csv")
        # load_to_firestore(aggregated)
    except Exception as e:
        print(e)


run()
