class InterventionEngine:

    def __init__(self, final_df):
        self.df = final_df.copy()

    def generate_interventions(self):

        def get_nudge(row):

            phase = row["behaviour_phase"]

            if phase == "Stable":
                return "Behaviour stable. No action required."

            elif phase == "Vulnerable":
                return "Spending patterns slightly increasing. Monitor closely."

            elif phase == "Build-Up":
                return "Impulse momentum rising. Consider reviewing recent purchases."

            elif phase == "High-Risk":
                return "High spending risk detected. Activate spending reminder or limit."

            else:  # Burst
                return "Critical impulse alert! Temporary spending lock recommended."

        self.df["intervention_message"] = self.df.apply(get_nudge, axis=1)

        return self.df