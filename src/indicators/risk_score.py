import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize each column in the DataFrame to a 0–100 scale using Min-Max scaling.
    """
    scaler = MinMaxScaler(feature_range=(0, 100))
    scaled = scaler.fit_transform(df.ffill().bfill())
    return pd.DataFrame(scaled, index=df.index, columns=df.columns)


def compute_weighted_risk_index(df: pd.DataFrame, weights: dict = None) -> pd.Series:
    """
    Compute a single Market Risk Index (0–100) as a weighted average of selected indicators.
    """
    if weights is None:
        weights = {col: 1.0 for col in df.columns}

    # Ensure weights cover only existing columns
    valid_cols = [col for col in df.columns if col in weights]
    df = df[valid_cols]

    # Normalize
    norm_df = normalize_df(df)

    # Weighting
    weight_array = np.array([weights[col] for col in valid_cols])
    weighted_risk = norm_df.dot(weight_array) / weight_array.sum()

    return weighted_risk.rename("Market Risk Score")


def categorize_risk(score: float) -> str:
    """
    Categorize the numeric risk score into descriptive levels.
    """
    if score >= 75:
        return "🟥 High Risk"
    elif score >= 50:
        return "🟧 Moderate Risk"
    elif score >= 25:
        return "🟨 Low Risk"
    else:
        return "🟩 Stable"


def attach_risk_score(df: pd.DataFrame, weights: dict = None) -> pd.DataFrame:
    """
    Append 'Market Risk Score' and 'Risk Category' to input DataFrame.
    """
    score_series = compute_weighted_risk_index(df, weights)
    df["Market Risk Score"] = score_series
    df["Risk Category"] = df["Market Risk Score"].apply(categorize_risk)
    return df
