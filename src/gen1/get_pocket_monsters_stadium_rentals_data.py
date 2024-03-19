from bs4 import BeautifulSoup
import requests
import time
import csv
import os

"""
This script assembles CSVs of available rental Pokemon for each cup
in the original Pocket Monsters Stadium, released only in Japan.
Data sourced from the Japanese Pokemon Wiki, which is significantly
more thorough in its rental documentation than the Western equivalent.

These tables come back in Japanese and as such will need to be translated.
"""

PM_STADIUM_URI = 'https://wiki.xn--rckteqa2e.com/wiki/%E3%83%AC%E3%83%B3%E3%82%BF%E3%83%AB%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E4%B8%80%E8%A6%A7_(%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E3%82%B9%E3%82%BF%E3%82%B8%E3%82%A2%E3%83%A0)'
response = requests.get(PM_STADIUM_URI)
soup = BeautifulSoup(response.content, 'html.parser')

# Find both 'table.bluetable's, which contain the two rental pools
bluetables = soup.find_all('table', class_='bluetable')
rental_tables = {
    'nintendo_cup_98': bluetables[0],
    'nintendo_cup_97': bluetables[1]
}

for cup, table in rental_tables.items():
    rows = table.find_all('tr')

    rental_data_list = []
    for row in rows[1:]:
        rental_data = {}
        rowheads = row.find_all('th')
        rowcols = row.find_all('td')

        rental_data['ID'] = rowheads[0].text.strip()
        rental_data['Name'] = rowheads[1].text.strip()

        rental_data['HP'] = rowcols[0].text.strip()
        rental_data['Attack'] = rowcols[1].text.strip()
        rental_data['Defense'] = rowcols[2].text.strip()
        rental_data['Speed'] = rowcols[3].text.strip()
        rental_data['Special'] = rowcols[4].text.strip()
        rental_data['Move1'] = rowcols[5].text.strip()
        rental_data['Move2'] = rowcols[6].text.strip()
        rental_data['Move3'] = rowcols[7].text.strip()
        rental_data['Move4'] = rowcols[8].text.strip()

        # print(rental_data)
        rental_data_list.append(rental_data)

    # print(rental_data_list)

    script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(
        script_dir,
        f'../../data/gen1/csv/pocket_monsters_stadium/{cup}_rentals.csv'
    )
    # print(file_path)

    with open(file_path, 'w+', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'ID', 'Name', 'HP', 'Attack', 'Defense', 'Speed', 'Special',
            'Move1', 'Move2', 'Move3', 'Move4'
        ])
        writer.writeheader()
        for pokemon in rental_data_list:
            writer.writerow(pokemon)

    print(f"Finished writing {cup}_rentals.csv")

time.sleep(10)  # to prevent IP ban if script gets spammed somehow
