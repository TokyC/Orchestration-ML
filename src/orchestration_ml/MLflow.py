import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

import mlflow
import mlflow.sklearn # Wrapper pour scikit-learn

from lightgbm.sklearn import LGBMClassifier
from sklearn.metrics import f1_score, PrecisionRecallDisplay, precision_recall_curve


def run_mlflow():
    X_train = pd.read_csv(os.path.expanduser("data/X_train.csv"))
    X_test = pd.read_csv(os.path.expanduser("data/X_test.csv"))
    y_train = pd.read_csv(os.path.expanduser("data/y_train.csv")).values.flatten()
    y_test = pd.read_csv(os.path.expanduser("data/y_test.csv")).values.flatten()

    # Hyper-paramètres des modèles
    hyp_params = {
        "num_leaves": 60,
        "min_child_samples": 10,
        "max_depth": 12,
        "n_estimators": 100,
        "learning_rate": 0.1
    }

    # Identification de l'interface MLflow
    mlflow.set_tracking_uri("file://" + os.path.expanduser('~/Desktop\Etudes\orchestration-ml\orchestration-ml\src\orchestration_ml\mlruns'))

    mlflow.set_experiment("orchestration-ml")

    with mlflow.start_run() as run:
        model = LGBMClassifier(**hyp_params, objective="multiclass", verbose=-1)
        model.fit(X_train, y_train)

        # On calcule le score du modèle sur le test
        score = f1_score(y_test, model.predict(X_test), average="weighted")

        mlflow.log_params(hyp_params)
        mlflow.log_metric("f1", score)

        print(mlflow.get_artifact_uri())
        mlflow.sklearn.log_model(model, "model")

if __name__ == "__main__":
    run_mlflow()