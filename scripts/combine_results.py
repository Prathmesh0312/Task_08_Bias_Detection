# scripts/combine_results.py

import os
import glob
import pandas as pd

def combine_results():
    # Path to results folder
    RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
    OUTPUT_PATH = os.path.join(RESULTS_DIR, "all_models_combined.csv")

    # Get all CSV files in results/
    csv_files = glob.glob(os.path.join(RESULTS_DIR, "*_bias_results.csv"))

    if not csv_files:
        print(" No CSV files found in results/. Ensure your files end with _bias_results.csv")
        return

    print(" Found CSV files:")
    for f in csv_files:
        print("   →", os.path.basename(f))

    # Read and combine robustly
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(
                file,
                encoding="utf-8",
                engine="python",
                on_bad_lines="skip"
            )
        except Exception as e1:
            print(f" UTF-8 failed for {file}, trying latin-1...")
            try:
                df = pd.read_csv(
                    file,
                    encoding="latin1",
                    engine="python",
                    on_bad_lines="skip"
                )
            except Exception as e2:
                print(f" Failed to parse {file}. Error: {e2}")
                continue

        dfs.append(df)




    combined_df = pd.concat(dfs, ignore_index=True)

    # Save combined
    combined_df.to_csv(OUTPUT_PATH, index=False)

    print("\n Combined CSV created successfully!")
    print(f" Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    combine_results()
