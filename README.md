# xG Thesis Project

Bachelor thesis project focused on Expected Goals (xG) modeling using StatsBomb Open Data.

## Objective

The goal of this project is to compare:

- Logistic Regression (with L1 regularization)
- Random Forest

for the estimation of Expected Goals (xG), using shot-level data from major international competitions.

The analysis focuses on:

- FIFA World Cup 2018
- FIFA World Cup 2022
- UEFA Euro 2020
- UEFA Euro 2024

---

## Project Structure
## 📁 Project Structure

```text
.
├── data/
│   ├── raw/
│   │   ├── matches/          # Downloaded match lists (not versioned)
│   │   └── events/           # Downloaded event data (not versioned)
│   └── processed/
│       ├── match_ids.json
│       └── shots_sample.csv
├── src/
│   ├── ingestion/
│   │   ├── download_matches.py
│   │   ├── extract_match_ids.py
│   │   └── download_events.py
│   └── preprocessing/
│       └── build_shots_dataset.py
└── README.md
```

---

## Data Pipeline

1. Select competitions and seasons.
2. Download match lists from StatsBomb Open Data.
3. Extract `match_id` for selected competitions.
4. Download event data for each match.
5. Build a shot-level dataset (1 row = 1 shot).
6. Exclude penalty kicks.
7. Prepare dataset for modeling.

All raw data are excluded from version control and can be regenerated using the ingestion scripts.

---

## Current Status

- ✅ Competitions selected
- ✅ Matches downloaded
- ✅ Match IDs extracted
- ✅ Events downloaded (sample)
- ✅ Shot-level sample dataset created
- ⏳ Feature selection
- ⏳ Modeling (Logistic vs Random Forest)
- ⏳ Evaluation (ROC, Calibration, RGA)

---

## Sample Dataset

A preliminary shot-level dataset (`shots_sample.csv`) has been generated using a sample of 20 matches to inspect:

- Available features
- Data structure
- Missing values
- Target variable definition

The full dataset will be built using all selected matches.

---

## Next Steps

- Feature engineering (distance, angle, contextual variables)
- Variable selection (correlation, multicollinearity, L1)
- Model training
- Performance comparison
- Calibration analysis

---

## Tools

- Python
- Pandas
- Scikit-learn
- StatsBomb Open Data
