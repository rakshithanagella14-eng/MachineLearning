"""
Day 36 requirement: Statistical summary & findings.
"""
import pandas as pd
import sqlite3
import numpy as np
from scipy import stats

conn = sqlite3.connect('ipl.db')
deliveries = pd.read_sql_query("SELECT * FROM deliveries", conn)
matches = pd.read_sql_query("SELECT * FROM matches", conn)
conn.close()

print("=" * 60)
print("  Descriptive statistics: runs per ball")
print("=" * 60)
print(f"Mean: {deliveries['total_runs'].mean():.3f}")
print(f"Variance: {deliveries['total_runs'].var():.3f}")
print(f"Std Dev: {deliveries['total_runs'].std():.3f}")
print(f"Skewness: {deliveries['total_runs'].skew():.3f}")

print("\nCorrelation: over number vs runs scored")
corr = deliveries[['over', 'total_runs']].corr().iloc[0,1]
print(f"Correlation coefficient: {corr:.3f}")

# Hypothesis test: do death overs (16-20) score significantly more than middle overs (7-15)?
death = deliveries[deliveries['over'] > 15]['total_runs']
middle = deliveries[(deliveries['over'] > 6) & (deliveries['over'] <= 15)]['total_runs']
t_stat, p_val = stats.ttest_ind(death, middle, equal_var=False)
print("\n" + "=" * 60)
print("  Hypothesis test: Death overs vs Middle overs run rate")
print("=" * 60)
print(f"Death overs mean: {death.mean():.3f} | Middle overs mean: {middle.mean():.3f}")
print(f"t-statistic: {t_stat:.3f}, p-value: {p_val:.4f}")
if p_val < 0.05:
    print("Result: Statistically significant difference (p < 0.05)")
else:
    print("Result: No statistically significant difference (p >= 0.05)")
