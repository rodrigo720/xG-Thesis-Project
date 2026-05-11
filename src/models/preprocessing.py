import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# parte preprocessing 
# preparazione delle feature e pulizia della tabella 

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = df.columns.str.strip()

    if "x" in df.columns:
        df = df.rename(columns={"x": "location_x"})

    if "y" in df.columns:
        df = df.rename(columns={"y": "location_y"})

    if "under_pressure" in df.columns:
        df["under_pressure"] = df["under_pressure"].fillna(False).astype(str)

    return df

def get_feature_columns():
    numeric_features = [
        "minute",
        "possession",
        "location_x",
        "location_y",
        "distance",
        "angle"
        ]
    
    categorical_feature=[
        "team.name",
        "play_pattern.name",
        "position.name",
        "under_pressure",
        "shot.type.name",
        "shot.technique.name",
        "shot.body_part.name"
        ]
    return numeric_features, categorical_feature

#costruzione della pipeline
def build_preprocessor():
    numeric_features, categorical_features = get_feature_columns() 


    # pipeline per dati numerici
    #1. Imputazione (riempimento buchi)
    numeric_transformer = Pipeline (steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",StandardScaler())
    ])

    # pipeline per dati categorici
    #1. Imputazione (riempimento buchi)
    #2. Encoder (conversione binario/numerico)
    categorical_transformer = Pipeline(steps=[
        ("imputer" , SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ],)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num",numeric_transformer,numeric_features),
            ("cat",categorical_transformer,categorical_features)
        ]
    )

    return preprocessor


    
