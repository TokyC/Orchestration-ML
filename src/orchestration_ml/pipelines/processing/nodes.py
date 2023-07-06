import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Dict, Any


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset
    :param dataset:
    :return: dataset
    """

    df[["Home Win", "Away Win", "Draw", "Over 2.5", "Under 2.5"]] = df[
        ["Home Win", "Away Win", "Draw", "Over 2.5", "Under 2.5"]
    ].applymap(lambda x: x.replace("?", ""))
    df = df.drop_duplicates()
    return dict(dataset=df)


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features
    :param df:
    :return:
    """

    df_code = df[["Home Team", "Code 1"]]

    # Compter le nombre de victoires à domicile pour chaque équipe
    home_wins = df[df["Winner"] == "H"]["Home Team"].value_counts()

    # Compter le nombre total de matchs à domicile pour chaque équipe
    home_matches = df["Home Team"].value_counts()

    # Calculer le pourcentage de victoires à domicile pour chaque équipe
    home_win_percentage = (home_wins / home_matches) * 100

    home_win_percentage = home_win_percentage.rename("Home Win %")

    # % win when the team is Away

    # Compter le nombre de victoires à domicile pour chaque équipe
    away_wins = df[df["Winner"] == "A"]["Away Team"].value_counts()

    # Compter le nombre total de matchs à domicile pour chaque équipe
    away_matches = df["Away Team"].value_counts()

    # Calculer le pourcentage de victoires à domicile pour chaque équipe
    away_win_percentage = (away_wins / away_matches) * 100

    # change the name of the column
    away_win_percentage = away_win_percentage.rename("Away Win %")

    # Calculer le nombre moyen de buts à domicile pour chaque équipe
    home_goals_mean = df.groupby("Home Team")["Home Goals"].mean()
    home_goals_mean = home_goals_mean.rename("Avg_Goal_Home")

    away_goals_mean = df.groupby("Away Team")["Away Goals"].mean()
    away_goals_mean = away_goals_mean.rename("Avg_Goal_Away")

    # Calculer le nombre moyen de buts concéder à domicile
    home_goals_concede_mean = df.groupby("Home Team")["Away Goals"].mean()
    home_goals_concede_mean = home_goals_concede_mean.rename("Avg_Goal_Concede_Home")

    away_goals_concede_mean = df.groupby("Away Team")["Home Goals"].mean()
    away_goals_concede_mean = away_goals_concede_mean.rename("Avg_Goal_Concede_Away")

    df_silver = pd.concat(
        [
            home_win_percentage,
            away_win_percentage,
            home_goals_mean,
            home_goals_concede_mean,
            away_goals_mean,
            away_goals_concede_mean,
        ],
        axis=1,
    )
    df_silver = df_silver.reset_index().rename(columns={"index": "Team"})

    df_code = df_code.rename(columns={"Home Team": "Team"})
    df_code = df_code.drop_duplicates()

    df_final = pd.merge(df_code, df_silver, on="Team", how="inner")

    return dict(dataset=df_final)


def create_dataset(df_final: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode features
    :param df:
    :return:
    """
    df_filtered = df[["Code 1", "Code 2", "Winner"]]
    merged_df = pd.merge(
        df_final, df_filtered, left_on="Code 1", right_on="Code 1", how="left"
    )

    merged_df_1 = merged_df.rename(
        columns={
            "Code 2_x": "Code 2",
            "Home Win %": "Home_Win_T1",
            "Away Win %": "Away_Win_T1",
            "Avg_Goal_Home": "Avg_Goal_Home_T1",
            "Avg_Goal_Concede_Home": "Avg_Goal_Concede_Home_T1",
            "Avg_Goal_Away": "Avg_Goal_Away_T1",
            "Avg_Goal_Concede_Away": "Avg_Goal_Concede_Away_T1",
        }
    )
    merged_df_1 = merged_df_1.drop("Team", axis=1)

    merged_df_2 = pd.merge(
        merged_df_1, df_final, left_on="Code 2", right_on="Code 1", how="left"
    )
    merged_df_2 = merged_df_2.drop("Team", axis=1)
    merged_df_final = merged_df_2.rename(
        columns={
            "Code 1_x": "Code_T1",
            "Home Win %": "Home_Win_T2",
            "Away Win %": "Away_Win_T2",
            "Avg_Goal_Home": "Avg_Goal_Home_T2",
            "Avg_Goal_Concede_Home": "Avg_Goal_Concede_Home_T2",
            "Avg_Goal_Away": "Avg_Goal_Away_T2",
            "Avg_Goal_Concede_Away": "Avg_Goal_Concede_Away_T2",
            "Code 1_y": "Code_T2",
        }
    )

    # Réarranger les colonnes
    train_df = merged_df_final[
        [
            "Home_Win_T1",
            "Away_Win_T1",
            "Avg_Goal_Home_T1",
            "Avg_Goal_Concede_Home_T1",
            "Avg_Goal_Away_T1",
            "Avg_Goal_Concede_Away_T1",
            "Home_Win_T2",
            "Away_Win_T2",
            "Avg_Goal_Home_T2",
            "Avg_Goal_Concede_Home_T2",
            "Avg_Goal_Away_T2",
            "Avg_Goal_Concede_Away_T2",
            "Winner",
        ]
    ]

    train_df = train_df.dropna()

    return dict(dataset=train_df)


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode features
    :param df:
    :return:
    """
    for label in ["Winner"]:
        # train_df[label] = train_df[label].astype(int)
        df.loc[df[label] == "nan", label] = "unknown"
        df.loc[:, label] = LabelEncoder().fit_transform(df.loc[:, label].copy())
    return dict(dataset=df)


def split_dataset(df: pd.DataFrame, test_ratio: float) -> Dict[str, Any]:
    """
    Split dataset
    :param test_ratio:
    :param df:
    :return:
    """
    X = df.drop("Winner", axis=1)
    y = df["Winner"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_ratio, random_state=1234
    )
    return dict(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
