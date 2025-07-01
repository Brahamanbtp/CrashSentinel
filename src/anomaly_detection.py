import pandas as pd
from sklearn.ensemble import IsolationForest

# Train Isolation Forest model
def train_isolation_forest(df: pd.DataFrame, contamination: float = 0.05) -> IsolationForest:
    """
    Train an Isolation Forest on given features.

    Args:
        df (pd.DataFrame): Data to train on.
        contamination (float): Expected proportion of anomalies.

    Returns:
        IsolationForest: Trained model.
    """
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(df)
    return model

# Detect anomalies and return labels
def detect_anomalies(model: IsolationForest, df: pd.DataFrame) -> pd.Series:
    """
    Predict anomalies in the data.

    Args:
        model (IsolationForest): Trained model.
        df (pd.DataFrame): Data to predict on.

    Returns:
        pd.Series: -1 for anomaly, 1 for normal.
    """
    predictions = model.predict(df)
    return pd.Series(predictions, index=df.index)

# Add anomaly flag column to a DataFrame
def append_anomaly_column(df: pd.DataFrame, model: IsolationForest, features: list, column_name: str = 'anomaly') -> pd.DataFrame:
    """
    Append anomaly results to original DataFrame.

    Args:
        df (pd.DataFrame): Original DataFrame.
        model (IsolationForest): Trained model.
        features (list): Feature column names.
        column_name (str): Name of the new column.

    Returns:
        pd.DataFrame: Updated DataFrame with anomaly flag.
    """
    subset = df[features].dropna()
    anomalies = model.predict(subset)
    df.loc[subset.index, column_name] = anomalies
    return df