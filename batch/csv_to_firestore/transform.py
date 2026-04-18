import pandas as pd
from datetime import datetime

def prepare_dates_for_firestore(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit toutes les datetime en datetime Python natif sur le Colonee InvoiceDate."""
    df = df.copy()
    
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    
    for col in datetime_cols:
        df[col] = df[col].dt.to_pydatetime()  
    
    print(f"✅ ({datetime_cols}){len(datetime_cols)} colonne(s) datetime convertie(s) pour Firestore")
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