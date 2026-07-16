# 🏏 IPL Mini Project — Data Analysis
**Avishkarana Andhra Summer Internship 2026 | Days 21–30**

---

## 📁 Project Structure

```
ipl-project/
├── ipl_matches.csv         ← Raw dataset (download from Kaggle)
├── clean.py                ← Day 22: Data cleaning & preprocessing
├── eda_analysis.py         ← Day 23 & 26: EDA + Visual stories (6 charts)
├── sql_analysis.py         ← Day 24: SQL analysis using SQLite
├── stats_insights.py       ← Day 25: Statistical insights
├── ipl_cleaned.csv         ← Output: cleaned dataset
├── ipl.db                  ← Output: SQLite database
└── chart1–6.png            ← Output: all charts
```

---

## 🚀 How to Run (in order)

```bash
# Step 1 — Download dataset from Kaggle and rename to ipl_matches.csv
# Place it inside the ipl-project folder

# Step 2 — Clean the data
python clean.py

# Step 3 — EDA + all charts
python eda_analysis.py

# Step 4 — SQL analysis
python sql_analysis.py

# Step 5 — Statistical insights
python stats_insights.py
```

---

## 📊 Key Insights

| # | Insight |
|---|---------|
| 1 | Mumbai Indians have the most IPL wins overall |
| 2 | Winning the toss gives ~52% chance of winning the match |
| 3 | Teams prefer to field first after winning the toss |
| 4 | Wankhede Stadium (Mumbai) hosts the most matches |
| 5 | Home teams have a measurable win rate advantage (~55%) |
| 6 | AB de Villiers / CH Gayle among top Player-of-Match awardees |

---

## 🔧 Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy
```

---

## 📅 Day Coverage

| Day | Task | File |
|-----|------|------|
| 21 | Problem statement | This README |
| 22 | Data cleaning | clean.py |
| 23 | EDA deep dive | eda_analysis.py |
| 24 | SQL analysis | sql_analysis.py |
| 25 | Statistical insights | stats_insights.py |
| 26 | Visual stories | eda_analysis.py (6 charts) |
| 27 | Dashboard | Power BI (import ipl_cleaned.csv) |
| 28–30 | Report & presentation | See PPT |

---

## 📤 Dataset Source
[IPL Complete Dataset 2008–2020 — Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
