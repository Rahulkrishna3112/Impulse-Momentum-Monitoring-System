import pandas as pd
import numpy as np


class MomentumEngine:

    def __init__(self, rolling_df):
        self.df = rolling_df.copy()

    def normalize_column(self, column):
        min_val = self.df[column].min()
        max_val = self.df[column].max()

        if max_val - min_val == 0:
            return 0

        return (self.df[column] - min_val) / (max_val - min_val)

    def compute_momentum_score(self):

        df = self.df

        # Normalize components
        df["acc_norm"] = self.normalize_column("acceleration")
        df["vol_norm"] = self.normalize_column("volatility")
        df["time_norm"] = self.normalize_column("time_compression")
        df["night_norm"] = self.normalize_column("night_ratio")
        df["cat_norm"] = self.normalize_column("unique_categories")

        # Weighted score
        df["impulse_momentum_score"] = (
            (df["acc_norm"] * 0.25) +
            (df["vol_norm"] * 0.20) +
            (df["time_norm"] * 0.20) +
            (df["night_norm"] * 0.15) +
            (df["cat_norm"] * 0.20)
        ) * 100

        return df