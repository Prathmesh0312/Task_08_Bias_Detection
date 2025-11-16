# Task_08_Bias_Detection

## *Bias Detection in LLM-Generated Data Narratives*

This project tests how different Large Language Models (LLMs) respond to the same dataset when the questions are worded differently.
The goal is to see whether models change their answers based on framing, assumptions, or nationality cues in the prompt, even though the data never changes.

Three LLMs were used:

ChatGPT

Gemini

DeepSeek

Three types of biases were tested:

Framing bias

Confirmation bias

Nationality influence bias

All responses were saved, combined, analyzed, visualized, and validated.
---

## Project folder Structure


LLM_BIAS_Experiment/

       \── data/       
              └── llm_ready_bowling_with_match_context.csv
       \── prompts/
              └── prompt_variations.py
       \── results/
              ├── chatgpt_bias_results.csv
              ├── gemini_bias_results.csv
              ├── deepseek_bias_results.csv
              └── all_models_combined.csv
       \── analysis/
              ├── sentiment_summary.csv
              ├── entity_counts.csv
              ├── combined_sentiment_entity.csv
              └── validation_report.csv
       \── notebooks/
              └── visualize_bias.ipynb
       \── scripts/
              ├── run_experiment.py
              ├── analyze_bias.py
              └── validate_claims.py
       └── REPORT.md


---

## Dataset
- File name: llm_ready_bowling_with_match_context.csv
- Scope: Bowling statistics including overs, wickets, economy rate, team, and match details.
- Source: Public cricket tournament records from the 2023–24 season.

---

## Install requirements

Use a virtual environment or run directly

pip install pandas numpy matplotlib seaborn textblob


---

### Running Project
- 1 Generate prompt variations
  Prompts are already created in : prompts/prompt_variations.py
  
- 2 Run the experiment using your own API Key
  If you want to automatically call LLMs: python scripts/run_experiment.py
  This generates CSV files in the results folder.
  
- 3 Combine and analyze responses
  Analyze sentiment, mentioned players, and patterns: python scripts/analyze_bias.py
  This creates:

    sentiment_summary.csv

    entity_counts.csv

    combined_sentiment_entity.csv
  
- 4 Validate the Accuracy and Check Hallucinations
  This script checks:

    whether the model mentioned real players

  whether stats (wickets/economy) were correct

  whether nationality is mentioned

  hallucinated players not in the dataset

Run: python scripts/validate_claims.py
Output saved in: analysis/validation_report.csv

- 5 Visualization results
  notebooks/visualize_bias.ipynb

## How to Add More Models or More Hypotheses
In run_experiment.py, add your new model ID:

    models = [
        "deepseek/deepseek-r1:free",
        "google/gemini-flash-1.5",
        "openai/gpt-4o-mini"
    ]



## Academic Notes

This work satisfies the following requirements:

Experiment design

Hypotheses

Prompt variations

Data collection

Analysis

Visualizations

Bias detection

Mitigation ideas

Final report
