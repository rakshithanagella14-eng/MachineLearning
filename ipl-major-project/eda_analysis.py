"""
Day 23 / Day 35 requirement: EDA deep dive + visual stories.
Generates 6 charts into /charts folder.
"""
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('ipl.db')
deliveries = pd.read_sql_query("SELECT * FROM deliveries", conn)
matches = pd.read_sql_query("SELECT * FROM matches", conn)
conn.close()

plt.style.use('seaborn-v0_8-darkgrid')

# 1. Runs by team
runs_by_team = deliveries.groupby('batting_team')['total_runs'].sum().sort_values(ascending=False)
plt.figure(figsize=(9,5))
runs_by_team.plot(kind='bar', color='#1f77b4')
plt.title('Total Runs by Team'); plt.ylabel('Runs'); plt.xticks(rotation=45, ha='right')
plt.tight_layout(); plt.savefig('charts/chart1_runs_by_team.png'); plt.close()

# 2. Top batsmen
top_batsmen = deliveries.groupby('batsman')['total_runs'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9,5))
top_batsmen.plot(kind='barh', color='#ff7f0e')
plt.title('Top 10 Run Scorers'); plt.xlabel('Runs'); plt.gca().invert_yaxis()
plt.tight_layout(); plt.savefig('charts/chart2_top_batsmen.png'); plt.close()

# 3. Top bowlers by wickets
top_bowlers = deliveries.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9,5))
top_bowlers.plot(kind='barh', color='#2ca02c')
plt.title('Top 10 Wicket Takers'); plt.xlabel('Wickets'); plt.gca().invert_yaxis()
plt.tight_layout(); plt.savefig('charts/chart3_top_bowlers.png'); plt.close()

# 4. Run rate by over
runrate_by_over = deliveries.groupby('over')['total_runs'].mean()
plt.figure(figsize=(9,5))
runrate_by_over.plot(kind='line', marker='o', color='#d62728')
plt.title('Average Runs per Ball by Over'); plt.xlabel('Over'); plt.ylabel('Avg Runs')
plt.tight_layout(); plt.savefig('charts/chart4_runrate_by_over.png'); plt.close()

# 5. Fours/sixes distribution
boundary_counts = deliveries['total_runs'].value_counts().sort_index()
plt.figure(figsize=(9,5))
boundary_counts.plot(kind='bar', color='#9467bd')
plt.title('Runs-per-ball Distribution'); plt.xlabel('Runs off ball'); plt.ylabel('Count')
plt.tight_layout(); plt.savefig('charts/chart5_runs_distribution.png'); plt.close()

# 6. Wins by team
wins_by_team = matches['winner'].value_counts()
plt.figure(figsize=(9,5))
wins_by_team.plot(kind='bar', color='#8c564b')
plt.title('Match Wins by Team'); plt.ylabel('Wins'); plt.xticks(rotation=45, ha='right')
plt.tight_layout(); plt.savefig('charts/chart6_wins_by_team.png'); plt.close()

print("6 charts saved to /charts")
print("\nSummary stats:\n", deliveries['total_runs'].describe())
