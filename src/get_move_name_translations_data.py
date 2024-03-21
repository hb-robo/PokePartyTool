"""
This script grabs a table of 

Data sourced from Bulbapedia. In theory this should renew itself every time
a new generation is released, but it's possible that the page will be updated
in a way that breaks this script. If that happens, the script will need to be
updated to reflect the new page structure.
"""

import time
import os
import csv

import requests
from bs4 import BeautifulSoup

POKEMON_NAME_TRANSLATIONS_URI = \
    'https://bulbapedia.bulbagarden.net/wiki/List_of_moves_in_other_languages'
response = requests.get(POKEMON_NAME_TRANSLATIONS_URI, timeout=5)

try:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all 'table.roundtable's, which contain per-generation translations.
    tables = soup.find_all('table', class_='roundy')
    move_translation_tables = {
        'move': tables[0],
        'z_move': tables[1],
        # tables[2] is list of Mystery Dungeon exclusive moves
        'shadow_move': tables[3],
        'gmax_move': tables[4]
    }

    for movepool, table in move_translation_tables.items():
        move_translation_data = []

        rows = table.find_all('tr')

        # first row is header that we will not use
        for row in rows[1:]:
            rowcols = row.find_all('td')
            move_translation_data.append(
                {
                    'move_id': rowcols[0].text.strip(),
                    'name_eng': rowcols[1].text.strip(),
                    'name_jp_kana': rowcols[2].text.strip(),
                }
            )


        # print(move_translation_data)

        script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, f'../data/csv/{movepool}_name_translations.csv')
        # print(file_path)

        with open(file_path, 'w+', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'move_id', 'name_eng', 'name_jp_kana'
            ])
            writer.writeheader()
            for row in move_translation_data:
                writer.writerow(row)

        print(f"Finished writing {movepool}_name_translations.csv")

except requests.exceptions.RequestException as e:
    print(e)

finally:
    time.sleep(10)  # to prevent IP ban if script gets spammed somehow
