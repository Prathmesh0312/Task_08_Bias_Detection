# Task_08_Bias_Detection

This repository contains my work for Research Task 08 – Bias Detection in LLM Data Narratives, using the same cricket bowling dataset analyzed in Task 07.

---

## Overview
The goal is to test whether Large Language Models produce biased or inconsistent narratives when analyzing identical cricket data under different prompt framings or demographic cues.

---

## Dataset
- File name: llm_ready_bowling_with_match_context.csv
- Scope: Bowling statistics including overs, wickets, economy rate, team, and match details.
- Source: Public cricket tournament records from the 2023–24 season.

---

## Planned LLMs
- ChatGPT
- DeepSeek
- Gemini 1.5 Pro

---

### Experimental Design
- Defined the experiment structure and process.
- Preparing 3 to 5 bias hypotheses and prompt pairs.
- Setting unbiased ground-truth references using verified cricket statistics.
- Creating repository folders for prompts, results, and analysis logs.

## Repository Structure
Task_08_Bias_Detection/
├── prompts/ 
├── results/ 
├── analysis/ 
├── experiment_design.docx 
└── README.md 

## Next Steps
- Finalize bias hypotheses and prompts.
- Run tests across 2 to 3 LLMs in Week 2.
- Analyze patterns quantitatively and qualitatively.
- Create final bias detection report 
