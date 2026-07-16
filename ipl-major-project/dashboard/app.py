"""
Day 37-38 requirement: Dashboard wireframing + development.
Run: streamlit run dashboard/app.py   (from project root)
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="IPL Analytics Dashboard", layout="wide")

conn = sqlite3.connect('ipl.db')
deliveries = pd.read_sql_query("SELECT * FROM deliveries", conn)
matches = pd.read_sql_query("SELECT * FROM matches", conn)
conn.close()

st.title("🏏 IPL Performance Analytics Dashboard")
st.caption("Major Project — Data Analysis Internship")

# KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", len(matches))
col2.metric("Total Runs Scored", int(deliveries['total_runs'].sum()))
col3.metric("Total Wickets", int(deliveries['is_wicket'].sum()))
col4.metric("Avg Runs/Ball", round(deliveries['total_runs'].mean(), 2))

st.divider()

# Filters
teams = sorted(deliveries['batting_team'].unique())
selected_team = st.selectbox("Filter by team (batting)", ["All"] + teams)
filtered = deliveries if selected_team == "All" else deliveries[deliveries['batting_team'] == selected_team]

c1, c2 = st.columns(2)

with c1:
    top_batsmen = filtered.groupby('batsman')['total_runs'].sum().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(top_batsmen, x='total_runs', y='batsman', orientation='h', title="Top 10 Run Scorers")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    top_bowlers = filtered.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_bowlers, x='is_wicket', y='bowler', orientation='h', title="Top 10 Wicket Takers")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    runrate = filtered.groupby('over')['total_runs'].mean().reset_index()
    fig3 = px.line(runrate, x='over', y='total_runs', markers=True, title="Average Run Rate by Over")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    wins = matches['winner'].value_counts().reset_index()
    wins.columns = ['team', 'wins']
    fig4 = px.bar(wins, x='team', y='wins', title="Match Wins by Team")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Raw Data Sample")
st.dataframe(filtered.head(50))
