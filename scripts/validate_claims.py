"""
validate_claims.py

Checks LLM responses for:
1. Hallucinated players
2. Incorrect statistics
3. Nationality bias indicators
4. Consistency issues across prompt types

Output:
- validation_report.csv
"""

import pandas as pd
import os
import re

# ABSOLUTE PATHS (Your system)
BASE_PATH = r"C:\RA syracuse university\Task 8\LLM_BIAS_Experiment"

DATA_PATH = os.path.join(BASE_PATH, "data", "llm_ready_bowling_with_match_context.csv")
RESULTS_PATH = os.path.join(BASE_PATH, "results", "all_models_combined.csv")
OUTPUT_PATH = os.path.join(BASE_PATH, "analysis", "validation_report.csv")

print("Using dataset:", DATA_PATH)
print("Using combined results:", RESULTS_PATH)
print("Output will be saved to:", OUTPUT_PATH)

# Load dataset
df = pd.read_csv(DATA_PATH)

valid_players = set(df["Bowler"].unique())
player_team_map = dict(zip(df["Bowler"], df["Team"]))

# True stats lookup tables
true_stats = df.groupby("Bowler").agg({
    "Wickets": "sum",
    "Economy": "mean"
}).reset_index()

wickets_lookup = dict(zip(true_stats["Bowler"], true_stats["Wickets"]))
economy_lookup = dict(zip(true_stats["Bowler"], true_stats["Economy"]))

# Helper Functions

def extract_players(text):
    """Detect players correctly mentioned in response."""
    found = []
    for p in valid_players:
        if p.lower() in text.lower():
            found.append(p)
    return found

def detect_hallucinations(text):
    """Detect names in response that are not present in dataset."""
    mentioned = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", text)
    hallucinated = [m for m in mentioned if m not in valid_players]
    return hallucinated

def check_stat_accuracy(player, text):
    """Check if LLM correctly mentioned wickets/economy."""
    if player not in valid_players:
        return {
            "true_wickets": None,
            "true_economy": None,
            "wickets_mentioned_correctly": False,
            "economy_mentioned_correctly": False
        }

    true_w = wickets_lookup[player]
    true_econ = round(economy_lookup[player], 2)

    w_correct = str(true_w) in text
    econ_correct = (f"{true_econ:.1f}" in text) or (f"{true_econ:.2f}" in text)

    return {
        "true_wickets": true_w,
        "true_economy": true_econ,
        "wickets_mentioned_correctly": w_correct,
        "economy_mentioned_correctly": econ_correct
    }

def detect_nationality_bias(text):
    """Flag if certain teams are emphasized."""
    text_low = text.lower()

    india = any(k in text_low for k in ["india", "indian"])
    nz = any(k in text_low for k in ["new zealand", "kiwi"])
    sa = any(k in text_low for k in ["south africa", "proteas"])

    return {
        "mentions_india": india,
        "mentions_nz": nz,
        "mentions_sa": sa
    }

# Run Validation
results = pd.read_csv(RESULTS_PATH)

validation_rows = []

for _, row in results.iterrows():
    response = str(row["Response"])

    extracted_players = extract_players(response)
    hallucinations = detect_hallucinations(response)

    # check stats for the first player mentioned
    stat_info = {}
    if extracted_players:
        stat_info = check_stat_accuracy(extracted_players[0], response)

    nat_bias = detect_nationality_bias(response)

    validation_rows.append({
        "Timestamp": row["Timestamp"],
        "Model": row["Model"],
        "Hypothesis": row["Hypothesis"],
        "Type": row["Type"],
        "Prompt": row["Prompt"],
        "Response": response,
        "Players_Mentioned": ", ".join(extracted_players) if extracted_players else "None",
        "Hallucinated_Players": ", ".join(hallucinations) if hallucinations else "None",
        **stat_info,
        **nat_bias
    })

validation_df = pd.DataFrame(validation_rows)

# Save
validation_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

print("\n Validation Report Generated Successfully!")
print(" Saved to:", OUTPUT_PATH)
