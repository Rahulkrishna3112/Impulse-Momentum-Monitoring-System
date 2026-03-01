#  Impulse Momentum Monitoring System (IMMS)

##  Overview

The Impulse Momentum Monitoring System (IMMS) is a Behavioural Analytics Engine designed to detect impulse build-up phases in financial behaviour.

Instead of identifying overspending after it occurs, this system predicts behavioural momentum escalation before high-risk spending bursts occur.

---

#  Problem Statement

Traditional financial monitoring systems detect risk only after excessive spending or default occurs. 

There is a gap in detecting early behavioural impulse signals such as:
- Sudden spending acceleration
- Volatile spending behaviour
- Increased night-time transactions
- Rapid transaction bursts

This system models behavioural momentum and classifies users into dynamic behavioural phases.

---

#  System Architecture

1. User Behaviour Simulation Engine  
2. Semi-Real-Time Transaction Generator  
3. Daily Behaviour Metrics  
4. Rolling Behaviour Intelligence (7-Day Window)  
5. Impulse Momentum Scoring Model  
6. Behaviour Phase State Machine  
7. Intervention Engine  
8. Interactive Risk Dashboard  

---

#  Dataset Information

## Dataset Type: Synthetic

### Why Synthetic?

There is no publicly available real-world dataset containing:
- Daily transaction behaviour
- Psychological impulse indicators
- Night spending patterns
- Rolling behavioural metrics

Since real behavioural impulse datasets are not publicly accessible due to privacy constraints, a synthetic behavioural dataset was generated.

---

## How Dataset Was Generated

A rule-based behavioural simulation model was built using:

- Normal distributions for spending amount
- Probability-based transaction frequency
- Behavioural parameters per user:
  - Base transaction probability
  - Base spending mean
  - Spending variability factor
  - Impulse sensitivity factor

For each user:
- 30 days of transactions were simulated
- Each day generates 0–3 transactions probabilistically
- Spending follows Gaussian distribution around personal mean
- Night transactions flagged if hour ≥ 22
- Category selection randomised from behavioural pool

Rolling behavioural features were then computed using a 7-day moving window.

---

## Dataset Size

- Total Users: 5,000
- Total Transactions: ~108,000
- Total Daily Behaviour Records: ~72,000
- Rolling Behaviour Records: ~72,000

---

## Feature Description

### Transaction-Level Features
- user_id
- date
- hour
- amount
- category

### Daily Behaviour Features
- daily_spend
- daily_txn_count
- night_txn_count
- night_ratio
- unique_categories

### Rolling Behaviour Features
- rolling_spend_mean
- acceleration
- volatility
- rolling_txn_mean
- time_compression

### Final Behavioural Features
- impulse_momentum_score (0–100)
- behaviour_phase
- phase_changed
- intervention_message

---

#  Impulse Momentum Score Model

Impulse Momentum Score is computed using weighted normalization:

- Acceleration (25%)
- Volatility (20%)
- Time Compression (20%)
- Night Ratio (15%)
- Category Drift (20%)

Score Range: 0 – 100

---

#  Behavioural Phases

Users dynamically transition between:

Stable → Vulnerable → Build-Up → High-Risk → Burst

Phase transitions are tracked daily.

---

#  Intervention Engine

Based on behavioural phase, the system generates automated nudges such as:

- Spending review reminders
- Risk alerts
- Cooling period suggestions
- Temporary lock recommendations

---

#  Dashboard Features

- System-wide risk distribution
- Escalation monitoring
- Top high-momentum users
- Individual user drill-down
- Impulse risk gauge
- Automated behavioural nudges

---

# Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

---

# to Run

```bash
pip install -r requirements.txt
python main.py
cd app
streamlit run dashboard.py