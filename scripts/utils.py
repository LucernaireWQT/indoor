from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split


def get_train_and_test_data(df: pd.DataFrame, test_size: float) -> Tuple:
    X = df.drop(["zone", "mesure"], axis=1)
    y = df["zone"]

    return tuple(train_test_split(X, y, test_size=test_size))
