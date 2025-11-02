# data_utils/pipeline.py

import pandas as pd
from tqdm import tqdm

def process_large_csv(file_path, chunk_size=10000):
    results = []
    with pd.read_csv(file_path, chunksize=chunk_size) as reader:
        for chunk in tqdm(reader, desc=f"Processing {file_path}"):
            # Insert your processing here (e.g., validation function, transformation, etc.)
            # For demo: just append row count
            results.append(len(chunk))
    return results

def monitor_file(filename):
    import time
    with open(filename) as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                print(line, end="")
            else:
                time.sleep(1)
