from pathlib import Path
import pandas as pd

def extract_sales(csv_path: str) -> pd.DataFrame:
    # return DataFrame from csv file
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")
    
    df = pd.read_csv(path)
    return df
