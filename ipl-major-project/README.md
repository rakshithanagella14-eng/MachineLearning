# IPL Performance Analytics — Major Project

Industry-style analytics project analyzing IPL match and ball-by-ball data to surface
team performance, top players, and scoring-pattern insights, built end to end:
data generation/cleaning → EDA → SQL analysis → statistics → interactive dashboard.

## Problem Statement
Analyze IPL ball-by-ball and match data to identify top-performing players, team
scoring patterns across overs, and statistically test whether death-over scoring
differs meaningfully from middle-over scoring — supporting strategy decisions
around powerplay and death-over play.

## Project Structure
```
ipl-major-project/
├── data/
│   ├── generate_data.py       # synthetic dataset generator (matches + deliveries)
│   ├── matches.csv
│   ├── deliveries.csv
│   ├── matches_cleaned.csv
│   └── deliveries_cleaned.csv
├── charts/                    # 6 EDA visualizations (PNG)
├── dashboard/
│   └── app.py                 # Streamlit interactive dashboard
├── clean.py                   # data cleaning & SQLite load
├── eda_analysis.py             # EDA + chart generation
├── sql_analysis.py             # SQL queries (JOIN, GROUP BY, HAVING)
├── stats_insights.py            # descriptive stats + hypothesis test
├── ipl.db                      # SQLite database
├── requirements.txt
└── README.md
```

## KPIs Tracked
1. Total runs per team
2. Top 10 run scorers
3. Top 10 wicket takers
4. Average run rate by over
5. Match win counts by team
6. High run-scoring overs (>15 runs)

## How to Run
```bash
pip install -r requirements.txt
python data/generate_data.py     # generates raw dataset
python clean.py                  # cleans data, builds ipl.db
python eda_analysis.py           # generates charts/
python sql_analysis.py           # prints SQL query results
python stats_insights.py         # prints statistical findings
streamlit run dashboard/app.py   # launches interactive dashboard
```

## Key Insights
- Wicket-taking and run-scoring are concentrated among a small group of top players,
  consistent with real IPL scoring patterns.
- Run rate does not vary dramatically over-by-over on average, but specific overs
  (esp. overs 10, 16, 20) show spikes >200 runs aggregated across matches — driven
  by acceleration phases (post-powerplay and death overs).
- A t-test comparing death-over (16–20) vs middle-over (7–15) scoring found no
  statistically significant difference in this dataset (p > 0.05), suggesting
  scoring acceleration is match-specific rather than a fixed pattern.

## Tech Stack
Python, Pandas, NumPy, SQLite, Matplotlib, SciPy, Streamlit, Plotly

## Author
RAKSHITHA — ECE, Final Year, SPMVV | Avishkarana Andhra Summer Internship
