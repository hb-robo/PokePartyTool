from bs4 import BeautifulSoup
import requests
import time
import csv
import os
from gen1_constants import TYPES

"""
This script assembles a list of all moves in Generation 1 of Pokemon,
with some very minor additional information that you might find in a
Pokedex.

The intent is for this CSV to be portable, so specific implementation
details of how the moves function will be left to the simulator classes
for the Pokemon and Battle System of each unique game.
"""


# Assemble list of Serebii's type-specific move pages.
# They don't have a page with all of them combined.
uri_list = {}
for type in TYPES:
    uri_type = type.lower()
    uri_list[uri_type] = \
        f'https://www.serebii.net/attackdex-rby/type/{uri_type}.shtml'

gen1_move_list = []
for uri_type, uri in uri_list.items():
    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all 'dextable' tables, which contain the move list data
    dextable = soup.find('table', class_='dextable')

    rows = dextable.find_all('tr')
    for row in rows[1:]:
        move_data = {}
        rowcols = row.find_all('td')

        move_data['Name'] = rowcols[0].text.strip()
        move_data['Type'] = uri_type.capitalize()
        move_data['PP'] = rowcols[2].text.strip()
        move_data['Attack'] = rowcols[3].text.strip()
        move_data['Accuracy'] = rowcols[4].text.strip()
        move_data['Description'] = rowcols[5].text.strip()

        # print(move_data)
        gen1_move_list.append(move_data)

    time.sleep(10)

# print(gen1_move_list)

script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '../../data/csv/gen1/gen1_move_list.csv')
print(file_path)

with open(file_path, 'w+', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'Name', 'Type', 'PP', 'Attack', 'Accuracy', 'Description'
    ])
    writer.writeheader()
    for move in gen1_move_list:
        writer.writerow(move)

print("Finished writing gen1_move_list.csv")
