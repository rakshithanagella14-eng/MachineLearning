import pandas as pd
import sqlite3

df = pd.read_csv('ipl_cleaned.csv')
df.columns = df.columns.str.strip()
conn = sqlite3.connect('ipl.db')
df.to_sql('deliveries', conn, if_exists='replace', index=False)
print("✅ Loaded into SQLite as table 'deliveries'\n")

# detect column names
runs_col    = next((c for c in ['total_runs','runs_total','batsman_runs'] if c in df.columns), 'total_runs')
batsman_col = next((c for c in ['batsman','batter'] if c in df.columns), 'batsman')
team_col    = 'batting_team'
bowl_col    = 'bowling_team'
match_col   = next((c for c in ['match_id','id'] if c in df.columns), 'match_id')
over_col    = 'over'
bowler_col  = 'bowler'

def Q(title, sql):
    print("=" * 55)
    print(f"📊 {title}")
    print("=" * 55)
    try:
        r = pd.read_sql_query(sql, conn)
        print(r.to_string(index=False))
    except Exception as e:
        print(f"  ⚠ Skipped: {e}")
    print()

Q("Total Runs Scored by Each Team", f"""
    SELECT {team_col} AS Team,
           SUM({runs_col}) AS Total_Runs,
           COUNT(DISTINCT {match_col}) AS Matches_Played
    FROM deliveries
    GROUP BY {team_col}
    ORDER BY Total_Runs DESC
""")

Q("Top 10 Run Scorers", f"""
    SELECT {batsman_col} AS Batsman,
           SUM({runs_col}) AS Total_Runs,
           COUNT(*) AS Balls_Faced,
           ROUND(SUM({runs_col})*100.0/COUNT(*), 1) AS Strike_Rate
    FROM deliveries
    GROUP BY {batsman_col}
    ORDER BY Total_Runs DESC
    LIMIT 10
""")

Q("Top 10 Wicket Takers", f"""
    SELECT {bowler_col} AS Bowler,
           SUM(is_wicket) AS Wickets,
           COUNT(DISTINCT {match_col}) AS Matches
    FROM deliveries
    GROUP BY {bowler_col}
    ORDER BY Wickets DESC
    LIMIT 10
""")

Q("Most Sixes by Team", f"""
    SELECT {team_col} AS Team,
           SUM(is_six) AS Total_Sixes,
           SUM(is_four) AS Total_Fours
    FROM deliveries
    GROUP BY {team_col}
    ORDER BY Total_Sixes DESC
""")

Q("Average Runs in Powerplay vs Death Overs", f"""
    SELECT
        CASE
            WHEN {over_col} <= 5  THEN 'Powerplay (1-6)'
            WHEN {over_col} <= 15 THEN 'Middle (7-15)'
            ELSE 'Death (16-20)'
        END AS Phase,
        ROUND(AVG({runs_col}), 3) AS Avg_Runs_Per_Ball,
        SUM({runs_col}) AS Total_Runs,
        SUM(is_wicket) AS Wickets_Lost
    FROM deliveries
    GROUP BY Phase
    ORDER BY Avg_Runs_Per_Ball DESC
""")

Q("Top 10 Most Dangerous Batting Pairs (Partnership runs)", f"""
    SELECT {batsman_col} AS Batsman, {team_col} AS Team,
           COUNT(DISTINCT {match_col}) AS Matches,
           SUM({runs_col}) AS Runs,
           SUM(is_six) AS Sixes
    FROM deliveries
    GROUP BY {batsman_col}, {team_col}
    HAVING Matches >= 10
    ORDER BY Runs DESC
    LIMIT 10
""")

Q("Wicket Types Distribution", """
    SELECT dismissal_kind AS Wicket_Type,
           COUNT(*) AS Count,
           ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM deliveries WHERE dismissal_kind != 'none'), 1) AS Pct
    FROM deliveries
    WHERE dismissal_kind != 'none'
    GROUP BY dismissal_kind
    ORDER BY Count DESC
""")

conn.close()
print("✅ All SQL queries done! ipl.db saved.")
