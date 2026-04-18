import pandas as pd

def extract(filepath: str) -> pd.DataFrame:
    """Load raw orders from a daily export file."""
    """The CSV file not formated in UTF-8 (Pandas default extraction) but in ISO-8859-1"""
    df = pd.read_csv(filepath, encoding='ISO-8859-1', parse_dates=["InvoiceDate"])
    print("✅ Extracted")
    return df