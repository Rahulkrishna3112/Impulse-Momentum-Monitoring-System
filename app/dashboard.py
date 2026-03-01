import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Impulse Momentum Monitoring System", layout="wide")

st.title("💳 Impulse Momentum Monitoring System")
st.subheader("Behavioural Risk Intelligence Dashboard")

df = pd.read_csv("../data/system_output.csv")
df["date"] = pd.to_datetime(df["date"])

latest_date = df["date"].max()
latest_df = df[df["date"] == latest_date]

# ---------------------------------
# OVERVIEW METRICS
# ---------------------------------
st.header("📊 System Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Users", latest_df["user_id"].nunique())
col2.metric("Build-Up", (latest_df["behaviour_phase"] == "Build-Up").sum())
col3.metric("High-Risk", (latest_df["behaviour_phase"] == "High-Risk").sum())
col4.metric("Burst", (latest_df["behaviour_phase"] == "Burst").sum())
col5.metric("Escalations Today", latest_df["phase_changed"].sum())

# ---------------------------------
# PHASE DISTRIBUTION
# ---------------------------------
st.header("📈 Behaviour Phase Distribution")

phase_counts = latest_df["behaviour_phase"].value_counts().reset_index()
phase_counts.columns = ["Phase", "Count"]

color_map = {
    "Stable": "green",
    "Vulnerable": "yellow",
    "Build-Up": "orange",
    "High-Risk": "red",
    "Burst": "darkred"
}

fig = px.bar(
    phase_counts,
    x="Phase",
    y="Count",
    color="Phase",
    color_discrete_map=color_map
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# TOP RISK USERS
# ---------------------------------
st.header("🔥 Top 10 High Momentum Users")

top_users = latest_df.sort_values(
    "impulse_momentum_score",
    ascending=False
).head(10)

st.dataframe(top_users[[
    "user_id",
    "impulse_momentum_score",
    "behaviour_phase"
]])

# ---------------------------------
# USER DRILL-DOWN
# ---------------------------------
st.header("🔍 User Behaviour Drill-Down")

selected_user = st.selectbox("Select User ID", df["user_id"].unique())
user_df = df[df["user_id"] == selected_user]

fig2 = px.line(
    user_df,
    x="date",
    y="impulse_momentum_score",
    title="Impulse Momentum Trend"
)

st.plotly_chart(fig2, use_container_width=True)

latest_user_row = user_df[user_df["date"] == latest_date]

if not latest_user_row.empty:

    current_phase = latest_user_row["behaviour_phase"].values[0]
    current_score = latest_user_row["impulse_momentum_score"].values[0]
    intervention = latest_user_row["intervention_message"].values[0]

    # Risk Gauge
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_score,
        title={"text": "Impulse Momentum Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "red"},
            "steps": [
                {"range": [0, 30], "color": "green"},
                {"range": [30, 55], "color": "yellow"},
                {"range": [55, 75], "color": "orange"},
                {"range": [75, 100], "color": "red"},
            ],
        },
    ))

    st.plotly_chart(gauge, use_container_width=True)

    st.subheader("📌 Current Status")
    st.write(f"**Phase:** {current_phase}")
    st.write(f"**Intervention:** {intervention}")