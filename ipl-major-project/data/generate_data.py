"""
Generates a realistic synthetic IPL dataset: matches.csv + deliveries.csv
Run once: python generate_data.py
"""
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

teams = ['Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Delhi Capitals', 'Sunrisers Hyderabad',
         'Rajasthan Royals', 'Punjab Kings']

batsmen_pool = ['R Sharma','V Kohli','MS Dhoni','KL Rahul','S Iyer','R Pant',
                'D Warner','J Bairstow','F du Plessis','Q de Kock','S Gill',
                'S Samson','H Pandya','A Rahane','R Gaikwad','Y Chahar_bat',
                'M Pandey','N Rana','P Shaw','I Kishan']

bowlers_pool = ['J Bumrah','Y Chahal','R Ashwin','T Boult','B Kumar','K Rabada',
                'R Jadeja','A Nortje','M Shami','J Archer','V Chakravarthy',
                'D Chahar','Harshal Patel','T Natarajan','Rashid Khan']

venues = ['Wankhede Stadium','M. A. Chidambaram Stadium','Eden Gardens',
          'Arun Jaitley Stadium','M. Chinnaswamy Stadium','Narendra Modi Stadium']

NUM_MATCHES = 60
rows_matches = []
rows_deliveries = []

for match_id in range(1, NUM_MATCHES + 1):
    t1, t2 = random.sample(teams, 2)
    venue = random.choice(venues)
    season = random.choice([2022, 2023, 2024, 2025])
    toss_winner = random.choice([t1, t2])
    toss_decision = random.choice(['bat', 'field'])
    winner = random.choice([t1, t2])
    margin = random.choice(['runs', 'wickets'])
    margin_val = random.randint(1, 60) if margin == 'runs' else random.randint(1, 9)

    rows_matches.append({
        'match_id': match_id, 'season': season, 'venue': venue,
        'team1': t1, 'team2': t2, 'toss_winner': toss_winner,
        'toss_decision': toss_decision, 'winner': winner,
        'win_margin_type': margin, 'win_margin': margin_val
    })

    # simulate deliveries for both innings
    for innings, (batting_team, bowling_team) in enumerate([(t1, t2), (t2, t1)], start=1):
        batsmen = random.sample(batsmen_pool, 6)
        bowlers = random.sample(bowlers_pool, 5)
        for over in range(1, 21):
            bowler = random.choice(bowlers)
            for ball in range(1, 7):
                batsman = random.choice(batsmen)
                runs = np.random.choice([0,1,2,3,4,6], p=[0.35,0.30,0.10,0.03,0.15,0.07])
                is_wicket = np.random.choice([0,1], p=[0.95,0.05])
                extras = np.random.choice([0,1], p=[0.92,0.08])
                rows_deliveries.append({
                    'match_id': match_id, 'innings': innings, 'over': over, 'ball': ball,
                    'batting_team': batting_team, 'bowling_team': bowling_team,
                    'batsman': batsman, 'bowler': bowler,
                    'total_runs': int(runs) + int(extras), 'is_wicket': int(is_wicket)
                })

matches_df = pd.DataFrame(rows_matches)
deliveries_df = pd.DataFrame(rows_deliveries)

matches_df.to_csv('matches.csv', index=False)
deliveries_df.to_csv('deliveries.csv', index=False)

print(f"matches.csv: {matches_df.shape}")
print(f"deliveries.csv: {deliveries_df.shape}")
