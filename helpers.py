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