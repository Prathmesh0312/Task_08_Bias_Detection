# scripts/analyze_bias.py

import os
import sys
import re
import pandas as pd

# ---------------- PATH SETUP ----------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

RESULTS_DIR = os.path.join(ROOT_DIR, "results")
ANALYSIS_DIR = os.path.join(ROOT_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)


def load_combined_results():
    """
    Load the combined CSV with all model outputs.
    Expects: results/all_models_combined.csv
    """
    path = os.path.join(RESULTS_DIR, "all_models_combined.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Combined results file not found at {path}. "
            f"Run combine_results.py first."
        )

    # Robust read (handles Excel-saved CSVs / weird encodings)
    try:
        df = pd.read_csv(path, encoding="utf-8", engine="python")
    except Exception:
        df = pd.read_csv(path, encoding="latin1", engine="python")

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Expect at least these columns (case-insensitive):
    # timestamp, model, hypothesis, type, prompt, response
    rename_map = {
        "timestamp": "timestamp",
        "model": "model",
        "hypothesis": "hypothesis",
        "type": "type",
        "prompt": "prompt",
        "response": "response",
    }
    df = df.rename(columns=rename_map)

    # Basic cleaning
    for col in ["model", "hypothesis", "type", "prompt", "response"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Normalize type labels (neutral/framed)
    if "type" in df.columns:
        df["type"] = df["type"].str.lower()

    return df


# ENTITY EXTRACTION 

ENTITY_REGEX = re.compile(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)")


def extract_entities(text: str):
    """
    Very simple entity extractor: grabs capitalized word sequences like
    'Mohammed Shami', 'Mitchell Santner', 'India', 'New Zealand'.
    """
    if not isinstance(text, str):
        return []
    matches = ENTITY_REGEX.findall(text)
    # Deduplicate but keep order
    seen = set()
    entities = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            entities.append(m)
    return entities


# SIMPLE SENTIMENT / POLARITY 

POSITIVE_WORDS = [
    "strong", "best", "effective", "balanced", "good", "excellent",
    "improvement", "improving", "consistent", "dominated", "better",
    "growth", "potential", "opportunity"
]

NEGATIVE_WORDS = [
    "struggling", "weak", "worst", "inconsistent", "poor",
    "high economy", "underperformed", "underperforming",
    "below expectations", "disappointing", "problem"
]


def sentiment_score(text: str):
    """
    Very lightweight sentiment-ish score:
    (#positive words) - (#negative words)
    """
    if not isinstance(text, str):
        return 0

    t = text.lower()
    pos = sum(t.count(w) for w in POSITIVE_WORDS)
    neg = sum(t.count(w) for w in NEGATIVE_WORDS)
    return pos - neg


def sentiment_label(score: int):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"


# MAIN ANALYSIS PIPELINE

def analyze_bias():
    df = load_combined_results()
    print(f"Loaded {len(df)} rows from all_models_combined.csv")

    #  ENTITY EXTRACTION
    df["entities"] = df["response"].apply(extract_entities)
    df["main_entity"] = df["entities"].apply(lambda lst: lst[0] if lst else None)

    # Explode to one row per (model, hypothesis, type, entity)
    df_entities = df.explode("entities")
    df_entities = df_entities.dropna(subset=["entities"])

    entity_counts = (
        df_entities
        .groupby(["model", "hypothesis", "type", "entities"])
        .size()
        .reset_index(name="count")
        .sort_values(["model", "hypothesis", "type", "count"], ascending=[True, True, True, False])
    )

    entity_out_path = os.path.join(ANALYSIS_DIR, "entity_counts.csv")
    entity_counts.to_csv(entity_out_path, index=False)
    print(f" Saved entity counts to: {entity_out_path}")

    # 2) SIMPLE SENTIMENT / POLARITY BY CONDITION
    df["sentiment_score"] = df["response"].apply(sentiment_score)
    df["sentiment_label"] = df["sentiment_score"].apply(sentiment_label)

    sentiment_summary = (
        df.groupby(["model", "hypothesis", "type"])
        .agg(
            avg_sentiment=("sentiment_score", "mean"),
            positive_share=("sentiment_label", lambda s: (s == "positive").mean()),
            negative_share=("sentiment_label", lambda s: (s == "negative").mean()),
        )
        .reset_index()
    )

    sentiment_out_path = os.path.join(ANALYSIS_DIR, "sentiment_summary.csv")
    sentiment_summary.to_csv(sentiment_out_path, index=False)
    print(f"Saved sentiment summary to: {sentiment_out_path}")

    #  PRINT HUMAN-READABLE SUMMARIES

    print("\n===== TOP ENTITIES PER MODEL / HYPOTHESIS / TYPE =====\n")
    for (model, hyp), sub in entity_counts.groupby(["model", "hypothesis"]):
        print(f"Model: {model} | Hypothesis: {hyp}")
        for t_type in ["neutral", "framed"]:
            sub_t = sub[sub["type"] == t_type]
            if sub_t.empty:
                continue
            top = sub_t.head(3)
            print(f"  - {t_type.upper()} → ", ", ".join(f"{row['entities']} (n={row['count']})"
                                                      for _, row in top.iterrows()))
        print()

    print("\n===== SENTIMENT SUMMARY (Neutral vs Framed) =====\n")
    for (model, hyp), sub in sentiment_summary.groupby(["model", "hypothesis"]):
        print(f"Model: {model} | Hypothesis: {hyp}")
        for t_type in ["neutral", "framed"]:
            row = sub[sub["type"] == t_type]
            if row.empty:
                continue
            r = row.iloc[0]
            avg = round(r["avg_sentiment"], 3)
            pos_pct = round(r["positive_share"] * 100, 1)
            neg_pct = round(r["negative_share"] * 100, 1)
            print(f"  - {t_type.upper()}: avg_sentiment={avg}, "
                  f"%positive={pos_pct}%, %negative={neg_pct}%")
        print()

    print("\n Bias analysis complete. Check the 'analysis/' folder for CSV outputs.\n")


if __name__ == "__main__":
    analyze_bias()
