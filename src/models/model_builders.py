from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from src.models.preprocessing import build_preprocessor

# parte dove definisco la pipeline (sklearn) in modo da dividere test set da training set 

def build_model(random_state : int = 42) : 
    preprocessor = build_preprocessor()

    #max_iter cerca i coeffinceti migliori
    #ho provato max_iter = 1000 ma non convergeva
    #seed fisso con random_state = 42
    models = {
        "logistic_regression" : Pipeline(steps=[
            ("preprocessing",preprocessor),
            ("smote", SMOTE(random_state = random_state)),
            ("model", LogisticRegression(max_iter=5000 , random_state= random_state))
        ]),

        "logistic_lasso" : Pipeline(steps=[                 # uso il valore c in valori logaritmici
            ("preprocessing", preprocessor),                # per migliorare il modello 
            ("smote",SMOTE(random_state = random_state)),          
            ("model", LogisticRegression(
                penalty = "l1",
                solver = "liblinear",
                max_iter = 5000,
                random_state = random_state
            ))
        ]),

        "random_forest" : Pipeline(steps=[
            ("prepocessing",preprocessor),
            ("smote",SMOTE(random_state = random_state)),
            ("model",RandomForestClassifier(
                n_estimators=300,
                random_state=random_state,
                class_weight=None
            ))
        ])
    }
    return models
