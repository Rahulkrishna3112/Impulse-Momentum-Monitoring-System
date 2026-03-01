import pandas as pd
import numpy as np


class BehaviourEngine:

    def __init__(self, transactions_df):
        self.transactions_df = transactions_df

    def compute_daily_metrics(self):

        df = self.transactions_df.copy()

        # Night Flag
        df["is_night"] = df["hour"].apply(lambda x: 1 if x >= 22 else 0)

        daily_metrics = df.groupby(["user_id", "date"]).agg(
            daily_spend=("amount", "sum"),
            daily_txn_count=("amount", "count"),
            night_txn_count=("is_night", "sum"),
            unique_categories=("category", "nunique")
        ).reset_index()

        # Night ratio
        daily_metrics["night_ratio"] = (
            daily_metrics["night_txn_count"] /
            daily_metrics["daily_txn_count"]
        )

        return daily_metrics

    def compute_rolling_metrics(self, daily_metrics_df):

        df = daily_metrics_df.copy()
        df = df.sort_values(["user_id", "date"])

        # Rolling 7-day spend mean
        df["rolling_spend_mean"] = (
            df.groupby("user_id")["daily_spend"]
            .rolling(window=7, min_periods=1)
            .mean()
            .reset_index(0, drop=True)
        )

        # Acceleration (difference from rolling mean)
        df["acceleration"] = df["daily_spend"] - df["rolling_spend_mean"]

        # Rolling volatility (std deviation)
        df["volatility"] = (
            df.groupby("user_id")["daily_spend"]
            .rolling(window=7, min_periods=1)
            .std()
            .reset_index(0, drop=True)
            .fillna(0)
        )

        # Rolling txn count mean
        df["rolling_txn_mean"] = (
            df.groupby("user_id")["daily_txn_count"]
            .rolling(window=7, min_periods=1)
            .mean()
            .reset_index(0, drop=True)
        )

        # Time compression proxy
        df["time_compression"] = df["daily_txn_count"] - df["rolling_txn_mean"]

        return df