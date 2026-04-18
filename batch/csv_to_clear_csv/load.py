import pandas as pd


def load(df: pd.DataFrame, output_path: str) -> None:
    """Write the aggregated result to the warehouse (here, a CSV)."""
    df.to_csv(output_path, index=False)
    print(f"✅ Loaded {len(df)} rows to {output_path}")