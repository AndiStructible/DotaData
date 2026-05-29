# DotaData

Binary classification project predicting Dota 2 match outcomes from 10-minute early-game snapshots.

## Overview

Match data is collected from the [OpenDota API](https://docs.opendota.com/), filtered for quality, and used to train machine learning models that predict whether the Radiant team wins — based only on information available at the 10-minute mark.

## Pipeline

```
match_data_compile.py  →  match_details_output.csv  →  MLDota.ipynb / MLDota_DecisionTree.ipynb
```

1. **`match_data_compile.py`** — fetches batches of parsed matches from the OpenDota API, applies quality filters, extracts features, and writes results to `match_details_output.csv`
2. **`MLDota.ipynb`** — Logistic Regression baseline model
3. **`MLDota_DecisionTree.ipynb`** — Decision Tree model with GridSearchCV hyperparameter tuning

## Match Filters

Only matches meeting all of the following criteria are included:

- Patch **7.41b** (patch ID 60)
- Game mode: **Ranked All Pick** (mode 22)
- All 10 players at **Divine rank or above** (rank tier ≥ 70)
- **No parties** — all players queued solo (party size = 1)
- Match duration **≥ 11 minutes** (660 seconds)
- Match must be **fully parsed** by OpenDota

## Features

All features are extracted at the **10-minute mark**:

| Feature | Description |
|---|---|
| `radiant_gold_div` | Radiant gold minus Dire gold |
| `radiant_xp_div` | Radiant XP minus Dire XP |
| `radiant_wards_div` | Radiant wards placed minus Dire wards placed |
| `radiant_towers_destroyed_div` | Radiant towers destroyed minus Dire towers destroyed |
| `radiant_first_blood` | 1 if Radiant scored first blood, 0 if Dire |

Absolute columns (`radiant_gold`, `dire_gold`, etc.) are also present in the CSV but excluded from the primary model due to multicollinearity with their divergence counterparts.

**Target:** `radiant_win` (True/False → 1/0)

## Setup

```bash
pip install requests
pip install pandas scikit-learn matplotlib seaborn notebook
```

## Usage

Collect match data:

```bash
python match_data_compile.py
```

This resumes automatically from where it left off if `match_details_2.json` already exists. Set `NUM_BATCHES` in the script to control how many batches of 100 matches are fetched per run.

Then open either notebook:

```bash
jupyter notebook MLDota.ipynb
jupyter notebook MLDota_DecisionTree.ipynb
```

## Files

| File | Description |
|---|---|
| `match_data_compile.py` | Data collection and feature extraction pipeline |
| `functions.py` | API calls, feature extraction helpers, and filter functions |
| `MLDota.ipynb` | Logistic Regression model and analysis |
| `MLDota_DecisionTree.ipynb` | Decision Tree model and analysis |
| `match_details_output.csv` | Processed dataset (git-ignored, generated locally) |
