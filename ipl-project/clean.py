import pandas as pd
import numpy as np

df = pd.read_csv('ipl_matches.csv')

print("=" * 55)
print("RAW DATA INFO")
print("=" * 55)
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 2 rows:")
print(df.head(2))

print("\n--- MISSING VALUES ---")
print(df.isnull().sum()[df.isnull().sum() > 0])

# ── Fix column names (strip spaces) ──────────────────────
df.columns = df.columns.str.strip()

# ── Drop duplicates ───────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
print(f"\nDuplicates removed: {before - len(df)}")

# ── Fill missing extras/dismissal columns ─────────────────
for col in ['extras_type', 'player_dismissed', 'dismissal_kind', 'fielder']:
    if col in df.columns:
        df[col] = df[col].fillna('none')

# ── Standardize team names ────────────────────────────────
team_rename = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Pune Warriors': 'Rising Pune Supergiant',
    'Rising Pune Supergiants': 'Rising Pune Supergiant',
}
for col in ['batting_team', 'bowling_team']:
    if col in df.columns:
        df[col] = df[col].replace(team_rename)

# ── Derived columns ───────────────────────────────────────
# Total runs per ball already exists; add is_boundary flag
if 'batsman_runs' in df.columns:
    df['is_four'] = (df['batsman_runs'] == 4).astype(int)
    df['is_six']  = (df['batsman_runs'] == 6).astype(int)

if 'player_dismissed' in df.columns:
    df['is_wicket'] = (df['player_dismissed'] != 'none').astype(int)

df.to_csv('ipl_cleaned.csv', index=False)
print("\nShape after cleaning:", df.shape)
print("\n✅ Saved → ipl_cleaned.csv")
