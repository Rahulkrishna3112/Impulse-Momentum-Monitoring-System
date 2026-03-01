import os
import pandas as pd
import datetime

from core.simulator import UserProfileGenerator, DailyTransactionSimulator
from core.behaviour_engine import BehaviourEngine
from core.momentum_engine import MomentumEngine
from core.phase_engine import PhaseEngine
from core.intervention_engine import InterventionEngine


if __name__ == "__main__":

    os.makedirs("data", exist_ok=True)

    # ---------------------------------
    # 1️⃣ Generate or Load Users
    # ---------------------------------
    if not os.path.exists("data/users.csv"):
        generator = UserProfileGenerator(num_users=5000)
        users_df = generator.generate_users()
        users_df.to_csv("data/users.csv", index=False)
        print("✅ Users generated successfully!")
    else:
        users_df = pd.read_csv("data/users.csv")
        print("✅ Users loaded successfully!")

    # ---------------------------------
    # 2️⃣ Simulate 30 Days Transactions
    # ---------------------------------
    simulator = DailyTransactionSimulator(users_df)

    start_date = datetime.date(2025, 1, 1)
    all_transactions = []

    for i in range(30):
        current_date = start_date + datetime.timedelta(days=i)
        daily_txns = simulator.simulate_one_day(current_date)
        all_transactions.append(daily_txns)

    transactions_df = pd.concat(all_transactions, ignore_index=True)

    transactions_df.to_csv("data/transactions.csv", index=False)

    print("✅ 30 Days Transactions Generated Successfully!")
    print(f"📊 Total Transactions: {len(transactions_df)}")

    # ---------------------------------
    # 3️⃣ Compute Daily Behaviour Metrics
    # ---------------------------------
    behaviour_engine = BehaviourEngine(transactions_df)
    daily_metrics_df = behaviour_engine.compute_daily_metrics()

    daily_metrics_df.to_csv("data/daily_metrics.csv", index=False)

    print("✅ Daily Behaviour Metrics Generated Successfully!")
    print(f"📊 Total Daily Metric Rows: {len(daily_metrics_df)}")

    # ---------------------------------
    # 4️⃣ Compute Rolling Behaviour Metrics
    # ---------------------------------
    rolling_df = behaviour_engine.compute_rolling_metrics(daily_metrics_df)

    rolling_df.to_csv("data/rolling_metrics.csv", index=False)

    print("✅ Rolling Behaviour Metrics Generated Successfully!")
    print(f"📊 Total Rolling Metric Rows: {len(rolling_df)}")

    # ---------------------------------
    # 5️⃣ Compute Impulse Momentum Score
    # ---------------------------------
    momentum_engine = MomentumEngine(rolling_df)
    momentum_df = momentum_engine.compute_momentum_score()

    momentum_df.to_csv("data/momentum_metrics.csv", index=False)

    print("✅ Impulse Momentum Score Generated Successfully!")

    # ---------------------------------
    # 6️⃣ Assign Behaviour Phases
    # ---------------------------------
    phase_engine = PhaseEngine(momentum_df)
    final_df = phase_engine.assign_phase()

    final_df.to_csv("data/final_behaviour_state.csv", index=False)

    print("✅ Behaviour Phases Assigned Successfully!")

    # ---------------------------------
    # 7️⃣ Generate Behavioural Interventions
    # ---------------------------------
    intervention_engine = InterventionEngine(final_df)
    system_output_df = intervention_engine.generate_interventions()

    system_output_df.to_csv("data/system_output.csv", index=False)

    print("✅ Intervention Engine Executed Successfully!")