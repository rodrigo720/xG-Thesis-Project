# xG Thesis Project

Bachelor thesis project focused on Expected Goals (xG) modeling using StatsBomb Open Data.

## Objective

The goal of this project is to compare:

- Logistic Regression (with L1 regularization)
- Random Forest

The analysis is performed on event data provided by **StatsBomb Open Data**.

## Dataset

The dataset used in the current analysis includes all matches from the **FIFA World Cup 2022**.

Dataset characteristics:

- 64 matches
- 1430 shots (penalties excluded)
- shot-level dataset (1 row = 1 shot)
Data source:

- StatsBomb Open Data

The dataset was constructed by extracting **shot events** from the full event data of each match.

---

## Project Structure
## 📁 Project Structure

```text
.
├── data/
│   ├── raw/                # Dati grezzi (immutabili)
│   └── processed/          # Dati puliti e trasformati (Dtypes ottimizzati)
├── src/
│   ├── ingestion/          # Script per il caricamento dei dati
│   ├── preprocessing/      # Pulizia, gestione NaN e casting dei tipi
│   └── analysis/           # Analisi esplorativa e calcoli statistici
├── reports/
│   └── figures/            # Grafici, diagrammi ed esportazioni
└── README.md
```



## Data Pipeline

The project includes a complete data pipeline implemented in Python.

Steps:

1. Select competitions and seasons
2. Download match metadata
3. Extract match IDs
4. Download event data for each match
5. Filter shot events
6. Build a shot-level dataset
7. Perform feature engineering and exploratory data analysis



## Feature Engineering

Several variables are derived from the raw data, including:

- Shot coordinates (x, y)
- Distance from goal
- Shooting angle
- Play pattern
- Shot type
- Body part used
- Player position
- Pressure indicator

The target variable is:

Goal=1
NoGoal=0


## Exploratory Data Analysis

Preliminary analysis includes:

- Goal vs non-goal distribution
- Shot distance distribution
- Goal probability by distance
- Shot distribution by body part
- Shot distribution by play pattern
- Goal rate under defensive pressure

These analyses help understand the structure of the dataset before model training.
---

### Distribuzione della Distanza dei Tiri - World Cup 2022
![Shot distance distribution](report/figures/distance_distribution_wc2022.png)

## Next Steps

- Feature engineering (distance, angle, contextual variables)
- Variable selection (correlation, multicollinearity, L1)
- Model training
- Performance comparison
- Calibration analysis



## Current Status

✔ Data pipeline implemented  
✔ Dataset construction (World Cup 2022)  
✔ Feature engineering  
✔ Exploratory data analysis  

Next steps:

- Variable selection
- Logistic Regression model
- Random Forest model
- Model evaluation (ROC, AUC, calibration)

## Tools

- Python
- Pandas
- Scikit-learn
- StatsBomb Open Data

Books:
- Hands-On Machine learning with Scikit-Learn,Keras and Tensorflow
- Python for Data Analysis
