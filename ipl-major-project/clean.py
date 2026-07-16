"""
Day 22 / Day 33 requirement: Data cleaning & preprocessing.
Loads raw matches.csv + deliveries.csv, cleans, saves cleaned versions + SQLite DB.
"""
import pandas as pd
import sqlite3

matches = pd.read_csv('data/matches.csv')
deliveries = pd.read_csv('data/deliveries.csv')

for df in (matches, deliveries):
    df.columns = df.columns.str.strip()
    df.drop_duplicates(inplace=True)

deliveries.dropna(subset=['batsman', 'bowler'], inplace=True)
deliveries['total_runs'] = deliveries['total_runs'].fillna(0).astype(int)
deliveries['is_wicket'] = deliveries['is_wicket'].fillna(0).astype(int)

matches.to_csv('data/matches_cleaned.csv', index=False)
deliveries.to_csv('data/deliveries_cleaned.csv', index=False)

conn = sqlite3.connect('ipl.db')
matches.to_sql('matches', conn, if_exists='replace', index=False)
deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)
conn.close()

print("Cleaned. Loaded into ipl.db as tables 'matches' and 'deliveries'.")
print(f"matches: {matches.shape}, deliveries: {deliveries.shape}")
