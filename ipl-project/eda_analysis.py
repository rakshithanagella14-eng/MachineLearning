import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="darkgrid")
plt.rcParams.update({
    'figure.facecolor': '#0d1117', 'axes.facecolor': '#161b22',
    'axes.labelcolor': 'white', 'xtick.color': 'white',
    'ytick.color': 'white', 'text.color': 'white', 'figure.dpi': 120
})
GOLD, BLUE, RED = '#FFD700', '#1f6aa5', '#e74c3c'

df = pd.read_csv('ipl_cleaned.csv')
df.columns = df.columns.str.strip()
print("✅ Loaded:", df.shape)
print("Columns:", df.columns.tolist())

# ── Aggregate: runs per match per team ───────────────────
runs_col   = next((c for c in ['total_runs','runs_total','batsman_runs'] if c in df.columns), None)
team_col   = 'batting_team' if 'batting_team' in df.columns else None
match_col  = next((c for c in ['match_id','id'] if c in df.columns), None)
bowl_col   = 'bowling_team' if 'bowling_team' in df.columns else None
over_col   = 'over' if 'over' in df.columns else None
batsman_col= next((c for c in ['batsman','batter'] if c in df.columns), None)
bowler_col = 'bowler' if 'bowler' in df.columns else None

print(f"\nUsing: runs={runs_col}, team={team_col}, match={match_col}")

# ════════════════════════════════════════════════════════
# CHART 1 — Total Runs Scored by Each Team
# ════════════════════════════════════════════════════════
if runs_col and team_col:
    team_runs = df.groupby(team_col)[runs_col].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(13, 6))
    colors = [GOLD if i == 0 else BLUE for i in range(len(team_runs))]
    bars = ax.bar(team_runs.index, team_runs.values, color=colors, edgecolor='black')
    ax.set_title('🏏 Total Runs Scored by Each IPL Team', fontsize=15, fontweight='bold', color=GOLD, pad=15)
    ax.set_xlabel('Team', fontsize=12); ax.set_ylabel('Total Runs', fontsize=12)
    plt.xticks(rotation=40, ha='right', fontsize=8)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+500,
                f"{int(bar.get_height()):,}", ha='center', fontsize=7, color='white')
    plt.tight_layout()
    plt.savefig('chart1_runs_by_team.png', bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print("✅ chart1_runs_by_team.png")

# ════════════════════════════════════════════════════════
# CHART 2 — Top 15 Run Scorers (Batsmen)
# ════════════════════════════════════════════════════════
if runs_col and batsman_col:
    top_batsmen = df.groupby(batsman_col)[runs_col].sum().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(13, 6))
    colors_b = sns.color_palette("YlOrRd", 15)
    bars = ax.bar(top_batsmen.index, top_batsmen.values, color=colors_b, edgecolor='black')
    ax.set_title('🏆 Top 15 Run Scorers in IPL History', fontsize=15, fontweight='bold', color=GOLD, pad=15)
    ax.set_xlabel('Batsman', fontsize=12); ax.set_ylabel('Total Runs', fontsize=12)
    plt.xticks(rotation=40, ha='right', fontsize=8)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
                str(int(bar.get_height())), ha='center', fontsize=7, color='white')
    plt.tight_layout()
    plt.savefig('chart2_top_batsmen.png', bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print("✅ chart2_top_batsmen.png")

# ════════════════════════════════════════════════════════
# CHART 3 — Top 15 Wicket Takers
# ════════════════════════════════════════════════════════
if 'is_wicket' in df.columns and bowler_col:
    top_bowlers = df.groupby(bowler_col)['is_wicket'].sum().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.barh(top_bowlers.index[::-1], top_bowlers.values[::-1],
                   color=sns.color_palette("Blues_r", 15), edgecolor='black')
    ax.set_title('🎯 Top 15 Wicket Takers in IPL History', fontsize=15, fontweight='bold', color=GOLD, pad=15)
    ax.set_xlabel('Total Wickets', fontsize=12)
    for bar in bars:
        ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                str(int(bar.get_width())), va='center', fontsize=9, color='white')
    plt.tight_layout()
    plt.savefig('chart3_top_bowlers.png', bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print("✅ chart3_top_bowlers.png")

# ════════════════════════════════════════════════════════
# CHART 4 — Run Rate by Over (Powerplay vs Death)
# ════════════════════════════════════════════════════════
if over_col and runs_col:
    over_runs = df.groupby(over_col)[runs_col].mean().reset_index()
    fig, ax = plt.subplots(figsize=(13, 5))
    colors_o = [RED if o >= 16 else (GOLD if o <= 5 else BLUE) for o in over_runs[over_col]]
    bars = ax.bar(over_runs[over_col], over_runs[runs_col], color=colors_o, edgecolor='black', linewidth=0.4)
    ax.set_title('📈 Average Runs Per Ball by Over (All IPL Matches)', fontsize=14, fontweight='bold', color=GOLD, pad=15)
    ax.set_xlabel('Over Number', fontsize=12); ax.set_ylabel('Avg Runs per Ball', fontsize=12)
    from matplotlib.patches import Patch
    legend = [Patch(color=GOLD, label='Powerplay (1-6)'),
              Patch(color=BLUE,  label='Middle Overs (7-15)'),
              Patch(color=RED,   label='Death Overs (16-20)')]
    ax.legend(handles=legend, loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.savefig('chart4_runrate_by_over.png', bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print("✅ chart4_runrate_by_over.png")

# ════════════════════════════════════════════════════════
# CHART 5 — Fours vs Sixes by Team
# ════════════════════════════════════════════════════════
if 'is_four' in df.columns and 'is_six' in df.columns and team_col:
    fours = df.groupby(team_col)['is_four'].sum()
    sixes = df.groupby(team_col)['is_six'].sum()
    combined = pd.DataFrame({'Fours': fours, 'Sixes': sixes}).sort_values('Sixes', ascending=False)
    fig, ax = plt.subplots(figsize=(13, 6))
    x = range(len(combined))
    w = 0.35
    ax.bar([i - w/2 for i in x], combined['Fours'], width=w, label='Fours', color=GOLD, edgecolor='black')
    ax.bar([i + w/2 for i in x], combined['Sixes'], width=w, label='Sixes', color=RED, edgecolor='black')
    ax.set_xticks(list(x)); ax.set_xticklabels(combined.index, rotation=40, ha='right', fontsize=8)
    ax.set_title('💥 Fours vs Sixes Hit by Each Team', fontsize=14, fontweight='bold', color=GOLD, pad=15)
    ax.set_ylabel('Count', fontsize=12); ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('chart5_fours_sixes.png', bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print("✅ chart5_fours_sixes.png")

# ════════════════════════════════════════════════════════
# CHART 6 — Dismissal Types Pie Chart
# ════════════════════════════════════════════════════════
if 'dismissal_kind' in df.columns:
    dismissals = df[df['dismissal_kind'] != 'none']['dismissal_kind'].value_counts()
    fig, ax = plt.subplots(figsize=(9, 7))
    colors_d = sns.color_palette("Set2", len(dismissals))
    ax.pie(dismissals.values, labels=dismissals.index, autopct='%1.1f%%',
           colors=colors_d, startangle=140, textprops={'color': 'white', 'fontsize': 9})
    ax.set_title('🎳 Wicket Types Distribution in IPL', fontsize=14, fontweight='bold', color=GOLD, pad=15)
    ax.set_facecolor('#161b22')
    plt.tight_layout()
    plt.savefig('chart6_dismissal_types.png', bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print("✅ chart6_dismissal_types.png")

print("\n🎉 All charts saved!")
