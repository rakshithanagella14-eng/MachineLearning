"""
Day 34 requirement: SQL data extraction (JOIN, GROUP BY, HAVING).
"""
import pandas as pd
import sqlite3

conn = sqlite3.connect('ipl.db')

def Q(title, sql):
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print(pd.read_sql_query(sql, conn))
    print()

Q("Top 5 Run Scorers", """
    SELECT batsman, SUM(total_runs) AS total_runs
    FROM deliveries GROUP BY batsman
    ORDER BY total_runs DESC LIMIT 5
""")

Q("Top 5 Wicket Takers", """
    SELECT bowler, SUM(is_wicket) AS wickets
    FROM deliveries GROUP BY bowler
    ORDER BY wickets DESC LIMIT 5
""")

Q("Team Win Counts (JOIN matches + deliveries not needed, matches only)", """
    SELECT winner, COUNT(*) AS wins
    FROM matches GROUP BY winner
    ORDER BY wins DESC
""")

Q("High-scoring overs (GROUP BY + HAVING)", """
    SELECT batting_team, over, SUM(total_runs) AS runs_in_over
    FROM deliveries
    GROUP BY batting_team, over
    HAVING runs_in_over > 15
    ORDER BY runs_in_over DESC LIMIT 10
""")

Q("JOIN: match result with venue", """
    SELECT m.match_id, m.venue, m.team1, m.team2, m.winner,
           SUM(d.total_runs) AS total_match_runs
    FROM matches m
    JOIN deliveries d ON m.match_id = d.match_id
    GROUP BY m.match_id
    ORDER BY total_match_runs DESC LIMIT 5
""")

conn.close()
