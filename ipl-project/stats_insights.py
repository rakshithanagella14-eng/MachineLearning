import pandas as pd
import numpy as np

df = pd.read_csv('ipl_cleaned.csv')
df.columns = df.columns.str.strip()

runs_col    = next((c for c in ['total_runs','runs_total','batsman_runs'] if c in df.columns), None)
batsman_col = next((c for c in ['batsman','batter'] if c in df.columns), None)
match_col   = next((c for c in ['match_id','id'] if c in df.columns), None)
over_col    = 'over' if 'over' in df.columns else None
bowler_col  = 'bowler' if 'bowler' in df.columns else None
team_col    = 'batting_team' if 'batting_team' in df.columns else None

print("=" * 55)
print("📐 STATISTICAL INSIGHTS — IPL BALL-BY-BALL DATA")
print("=" * 55)

# ── 1. Dataset Overview ───────────────────────────────
print("\n1️⃣  DATASET OVERVIEW")
print(f"   Total deliveries : {len(df):,}")
if match_col:
    print(f"   Total matches    : {df[match_col].nunique():,}")
if team_col:
    print(f"   Unique teams     : {df[team_col].nunique()}")
if runs_col:
    print(f"   Total runs scored: {df[runs_col].sum():,}")

# ── 2. Batting Stats ──────────────────────────────────
if runs_col and batsman_col and match_col:
    print("\n2️⃣  TOP BATSMEN STATS")
    agg_dict = {
        'Runs': (runs_col, 'sum'),
        'Balls': (runs_col, 'count'),
    }
    if 'is_four' in df.columns:
        agg_dict['Fours'] = ('is_four', 'sum')
    if 'is_six' in df.columns:
        agg_dict['Sixes'] = ('is_six', 'sum')
    bat = df.groupby(batsman_col).agg(**agg_dict).reset_index()
    bat['Strike_Rate'] = (bat['Runs'] / bat['Balls'] * 100).round(1)
    bat = bat[bat['Balls'] >= 100].sort_values('Runs', ascending=False).head(10)
    print(bat[[batsman_col, 'Runs', 'Balls', 'Strike_Rate']].to_string(index=False))

# ── 3. Bowling Stats ──────────────────────────────────
if 'is_wicket' in df.columns and bowler_col and runs_col:
    print("\n3️⃣  TOP BOWLERS STATS")
    bowl = df.groupby(bowler_col).agg(
        Wickets=('is_wicket', 'sum'),
        Runs_Given=(runs_col, 'sum'),
        Balls=(runs_col, 'count'),
    ).reset_index()
    bowl['Economy'] = (bowl['Runs_Given'] / (bowl['Balls']/6)).round(2)
    bowl = bowl[bowl['Balls'] >= 60].sort_values('Wickets', ascending=False).head(10)
    print(bowl[[bowler_col, 'Wickets', 'Economy']].to_string(index=False))

# ── 4. Phase Analysis ─────────────────────────────────
if over_col and runs_col:
    print("\n4️⃣  RUN RATE BY PHASE")
    df['phase'] = pd.cut(df[over_col], bins=[-1,5,15,20],
                         labels=['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)'])
    phase = df.groupby('phase', observed=True)[runs_col].agg(['mean','sum','count'])
    phase.columns = ['Avg_per_ball','Total_Runs','Deliveries']
    phase['Proj_per_over'] = (phase['Avg_per_ball']*6).round(2)
    print(phase.to_string())

# ── 5. Boundary Analysis ──────────────────────────────
if 'is_four' in df.columns and 'is_six' in df.columns:
    total = len(df)
    fours = df['is_four'].sum()
    sixes = df['is_six'].sum()
    print(f"\n5️⃣  BOUNDARY ANALYSIS")
    print(f"   Total Fours : {int(fours):,}  ({fours/total*100:.1f}% of deliveries)")
    print(f"   Total Sixes : {int(sixes):,}  ({sixes/total*100:.1f}% of deliveries)")
    print(f"   Boundary %  : {(fours+sixes)/total*100:.1f}%")
    if team_col:
        top_six_team = df.groupby(team_col)['is_six'].sum().idxmax()
        print(f"   Most Sixes Team: {top_six_team}")

# ── 6. Dismissal Stats ────────────────────────────────
if 'dismissal_kind' in df.columns:
    print("\n6️⃣  DISMISSAL BREAKDOWN")
    d = df[df['dismissal_kind'] != 'none']['dismissal_kind'].value_counts()
    for kind, count in d.items():
        print(f"   {kind:25} {count:5,}  ({count/d.sum()*100:.1f}%)")

# ── 7. Most Economical Bowlers ────────────────────────
if over_col and runs_col and bowler_col:
    print("\n7️⃣  MOST ECONOMICAL BOWLERS (min 300 balls)")
    eco = df.groupby(bowler_col).agg(
        balls=(runs_col,'count'), runs=(runs_col,'sum')).reset_index()
    eco = eco[eco['balls'] >= 300]
    eco['economy'] = (eco['runs']/(eco['balls']/6)).round(2)
    eco = eco.sort_values('economy').head(8)
    print(eco[[bowler_col,'balls','runs','economy']].to_string(index=False))

print("\n✅ Statistical analysis complete!")
