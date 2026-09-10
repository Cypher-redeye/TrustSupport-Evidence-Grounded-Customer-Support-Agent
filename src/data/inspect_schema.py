import os
import pandas as pd
from pathlib import Path
from src.config import settings

def find_dataset(raw_dir: Path) -> Path | None:
    for path in raw_dir.rglob("*.csv"):
        if path.name.lower() == "twcs.csv":
            return path
    return None

def inspect_dataset():
    raw_dir = Path(settings.raw_data_dir)
    dataset_file = find_dataset(raw_dir)
    
    if not dataset_file:
        print("Dataset not found!")
        return
        
    print(f"File path: {dataset_file}")
    print(f"File size: {dataset_file.stat().st_size / (1024*1024):.2f} MB")
    
    total_rows = 0
    missing_counts = None
    columns = None
    
    chunk_size = 100000
    for chunk in pd.read_csv(dataset_file, chunksize=chunk_size, dtype=str):
        if columns is None:
            columns = chunk.columns.tolist()
            missing_counts = pd.Series(0, index=columns)
            
        total_rows += len(chunk)
        missing_counts += chunk.isna().sum()
        
    print(f"Number of rows: {total_rows}")
    print(f"Number of columns: {len(columns)}")
    print(f"Column names: {columns}")
    print("Missing value counts:")
    for col, count in missing_counts.items():
        print(f"  {col}: {count}")

if __name__ == "__main__":
    inspect_dataset()
