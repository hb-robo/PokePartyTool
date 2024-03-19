from bs4 import BeautifulSoup
import requests
import time
import csv
import os

"""
This script grabs a table of experience values and thresholds for a Pokemon
based on their prescribed experience curve. The raw table functions as two
side-by-side tables, but this script merges the two into something more
queryable.

Two of these curves are only accessible Gen 3 and after, but the formulation
for the original four never changed over the years, making this a universal
table for all generations.

Data sourced from Bulbapedia.
"""

EXP_CURVES_URI = 'https://bulbapedia.bulbagarden.net/wiki/Experience'
response = requests.get(EXP_CURVES_URI)
soup = BeautifulSoup(response.content, 'html.parser')

# Find first 'table.roundy', which contains the experience curve data.
table = soup.find('table', class_='roundy')
rows = table.find_all('tr')

experience_curve_data = []

# first two rows are headers that we will not use
for row in rows[2:]:
    rowcols = row.find_all('td')
    level = rowcols[6].text.strip()

    experience_curve_data.append(
        {
            'level': level,
            'curve': 'Erratic',
            'total_exp_at_level': rowcols[0].text.strip(),
            'exp_to_next_level': rowcols[7].text.strip()
        }
    )
    experience_curve_data.append(
        {
            'level': level,
            'curve': 'Fast',
            'total_exp_at_level': rowcols[1].text.strip(),
            'exp_to_next_level': rowcols[8].text.strip()
        }
    )
    experience_curve_data.append(
        {
            'level': level,
            'curve': 'Medium Fast',
            'total_exp_at_level': rowcols[2].text.strip(),
            'exp_to_next_level': rowcols[9].text.strip()
        }
    )
    experience_curve_data.append(
        {
            'level': level,
            'curve': 'Medium Slow',
            'total_exp_at_level': rowcols[3].text.strip(),
            'exp_to_next_level': rowcols[10].text.strip()
        }
    )
    experience_curve_data.append(
        {
            'level': level,
            'curve': 'Slow',
            'total_exp_at_level': rowcols[4].text.strip(),
            'exp_to_next_level': rowcols[11].text.strip()
        }
    )
    experience_curve_data.append(
        {
            'level': level,
            'curve': 'Fluctuating',
            'total_exp_at_level': rowcols[5].text.strip(),
            'exp_to_next_level': rowcols[12].text.strip()
        }
    )

print(experience_curve_data)

script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '../data/csv/experience_curves.csv')
# print(file_path)

with open(file_path, 'w+', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'level', 'curve', 'total_exp_at_level', 'exp_to_next_level'
    ])
    writer.writeheader()
    for row in experience_curve_data:
        writer.writerow(row)

print("Finished writing experience_curves.csv")

time.sleep(10)  # to prevent IP ban if script gets spammed somehow
