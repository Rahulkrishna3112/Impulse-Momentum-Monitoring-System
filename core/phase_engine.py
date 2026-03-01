import pandas as pd


class PhaseEngine:

    def __init__(self, momentum_df):
        self.df = momentum_df.copy()

    def assign_phase(self):

        def get_phase(score):
            if score < 30:
                return "Stable"
            elif score < 55:
                return "Vulnerable"
            elif score < 75:
                return "Build-Up"
            elif score < 90:
                return "High-Risk"
            else:
                return "Burst"

        self.df["behaviour_phase"] = self.df["impulse_momentum_score"].apply(get_phase)

        # Sort properly
        self.df = self.df.sort_values(["user_id", "date"])

        # Detect phase transitions
        self.df["previous_phase"] = (
            self.df.groupby("user_id")["behaviour_phase"].shift(1)
        )

        self.df["phase_changed"] = (
            self.df["behaviour_phase"] != self.df["previous_phase"]
        )

        self.df["phase_changed"] = self.df["phase_changed"].fillna(False)

        return self.df