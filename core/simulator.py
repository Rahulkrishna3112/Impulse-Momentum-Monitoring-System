import pandas as pd
import numpy as np
import random


# -----------------------------------
# 1️⃣ USER PROFILE GENERATOR
# -----------------------------------
class UserProfileGenerator:
    def __init__(self, num_users=5000):
        self.num_users = num_users

    def generate_users(self):
        users = []

        behaviour_types = (
            ["Disciplined"] * int(0.40 * self.num_users) +
            ["Weekend_Impulse"] * int(0.25 * self.num_users) +
            ["Emotional_Night"] * int(0.20 * self.num_users) +
            ["Salary_Splurger"] * int(0.15 * self.num_users)
        )

        random.shuffle(behaviour_types)

        for i in range(self.num_users):
            behaviour = behaviour_types[i]

            if behaviour == "Disciplined":
                impulse_sensitivity = np.random.uniform(0.3, 0.5)
                self_control = np.random.uniform(0.6, 0.8)
                base_spend = np.random.normal(800, 100)
                base_txn_prob = 0.4

            elif behaviour == "Weekend_Impulse":
                impulse_sensitivity = np.random.uniform(0.5, 0.7)
                self_control = np.random.uniform(0.4, 0.6)
                base_spend = np.random.normal(1000, 200)
                base_txn_prob = 0.5

            elif behaviour == "Emotional_Night":
                impulse_sensitivity = np.random.uniform(0.7, 0.9)
                self_control = np.random.uniform(0.2, 0.5)
                base_spend = np.random.normal(600, 300)
                base_txn_prob = 0.6

            else:  # Salary_Splurger
                impulse_sensitivity = np.random.uniform(0.5, 0.8)
                self_control = np.random.uniform(0.3, 0.6)
                base_spend = np.random.normal(1500, 400)
                base_txn_prob = 0.5

            users.append([
                i + 1,
                behaviour,
                round(impulse_sensitivity, 3),
                round(self_control, 3),
                round(abs(base_spend), 2),
                base_txn_prob
            ])

        columns = [
            "user_id",
            "behaviour_type",
            "impulse_sensitivity",
            "self_control_factor",
            "base_spend_mean",
            "base_txn_probability"
        ]

        return pd.DataFrame(users, columns=columns)


# -----------------------------------
# 2️⃣ DAILY TRANSACTION SIMULATOR
# -----------------------------------
class DailyTransactionSimulator:
    def __init__(self, users_df):
        self.users_df = users_df
        self.categories = ["Food", "Fashion", "Electronics", "Travel", "Entertainment"]

    def simulate_one_day(self, current_date):
        transactions = []

        for _, user in self.users_df.iterrows():

            # Decide if user transacts today
            if np.random.rand() < user["base_txn_probability"]:

                txn_count = np.random.randint(1, 3)

                for _ in range(txn_count):

                    amount = abs(np.random.normal(
                        user["base_spend_mean"],
                        user["base_spend_mean"] * 0.3
                    ))

                    category = np.random.choice(self.categories)

                    # Normal time range
                    hour = np.random.randint(8, 23)

                    # Emotional night users more likely to transact late
                    if user["behaviour_type"] == "Emotional_Night":
                        if np.random.rand() < 0.4:
                            hour = np.random.randint(22, 24)

                    transactions.append([
                        user["user_id"],
                        current_date,
                        hour,
                        round(amount, 2),
                        category
                    ])

        columns = ["user_id", "date", "hour", "amount", "category"]

        return pd.DataFrame(transactions, columns=columns)