"""
Member B — Day 2
Merge Member A's Kyber results and Member B's Dilithium results into one
clean dataset.csv, handle missing/bad values, and confirm row count.

Use this if A and B ran their benchmarks on SEPARATE machines and have
two separate CSV files to combine. If both of you appended to the SAME
shared dataset.csv (e.g. via git), you can skip the merge step and just
run clean_dataset() directly on data/dataset.csv.
"""

import pandas as pd
import os

DATA_DIR = "data"
FINAL_PATH = os.path.join(DATA_DIR, "dataset.csv")


def merge_csvs(file_a: str, file_b: str, output_path: str = FINAL_PATH) -> pd.DataFrame:
    """Combines two CSVs with the same schema into one, removing exact duplicate rows."""
    df_a = pd.read_csv(file_a)
    df_b = pd.read_csv(file_b)

    print(f"File A: {len(df_a)} rows | File B: {len(df_b)} rows")

    # Sanity check: columns must match before merging
    if list(df_a.columns) != list(df_b.columns):
        print("WARNING: Column mismatch between files!")
        print(f"  File A columns: {list(df_a.columns)}")
        print(f"  File B columns: {list(df_b.columns)}")
        raise ValueError("Cannot merge — schemas don't match. Re-sync with Member A first.")

    merged = pd.concat([df_a, df_b], ignore_index=True)
    merged = merged.drop_duplicates()

    merged.to_csv(output_path, index=False)
    print(f"Merged dataset saved to {output_path} ({len(merged)} rows after deduplication)")
    return merged


def clean_dataset(path: str = FINAL_PATH) -> pd.DataFrame:
    """Handles missing values and confirms data quality before Phase 3."""
    df = pd.read_csv(path)
    original_len = len(df)

    print(f"\n--- Cleaning {path} ---")
    print(f"Starting rows: {original_len}")

    # Drop rows where the operation failed (success == 0) — these are
    # not useful for training the AI model on "best" choices
    failed_count = (df["success"] == 0).sum()
    if failed_count > 0:
        print(f"Found {failed_count} failed rows (success=0) — keeping them for now, "
              f"but flagging for review.")

    # Check for any missing values in critical numeric columns
    critical_cols = ["data_size_bytes", "latency_ms", "cpu_load_percent",
                      "time_taken_ms", "key_size_bytes", "output_size_bytes"]
    missing_before = df[critical_cols].isnull().sum().sum()
    if missing_before > 0:
        print(f"Found {missing_before} missing values in critical columns — dropping those rows.")
        df = df.dropna(subset=critical_cols)

    # Remove any rows with negative or zero time (clearly invalid measurements)
    invalid_time = (df["time_taken_ms"] <= 0).sum()
    if invalid_time > 0:
        print(f"Found {invalid_time} rows with invalid time_taken_ms — removing.")
        df = df[df["time_taken_ms"] > 0]

    df = df.drop_duplicates()

    print(f"Final rows after cleaning: {len(df)}")
    df.to_csv(path, index=False)

    # The key checkpoint from the plan: confirm at least 400 rows
    if len(df) >= 400:
        print(f"Row count check PASSED: {len(df)} >= 400 rows")
    else:
        print(f"Row count check FAILED: only {len(df)} rows (need 400+). "
              f"Run more benchmark combinations or add more network conditions.")

    return df


if __name__ == "__main__":
    # OPTION 1: If you have two separate files to merge, uncomment and edit these paths:
    # merge_csvs("data/dataset_member_a.csv", "data/dataset_member_b.csv")

    # OPTION 2: If you're both appending to the same shared dataset.csv already,
    # just run the cleaning step directly:
    clean_dataset(FINAL_PATH)