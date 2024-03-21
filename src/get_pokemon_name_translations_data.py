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
    'https://bulbapedia.bulbagarden.net/wiki/List_of_Japanese_Pok%C3%A9mon_names'
response = requests.get(POKEMON_NAME_TRANSLATIONS_URI, timeout=5)
try:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all 'table.roundtable's, which contain per-generation translations.
    tables = soup.find_all('table', class_='roundtable')

    pokemon_translation_data = []
    for table in tables:
        rows = table.find_all('tr')

        # first two rows are headers that we will not use
        for row in rows[2:]:
            rowcols = row.find_all('td')
            pokemon_translation_data.append(
                {
                    'id': rowcols[0].text.strip(),
                    'name_eng': rowcols[2].text.strip(),
                    'name_jp_kana': rowcols[3].text.strip(),
                }
            )


    print(pokemon_translation_data)

    script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '../data/csv/pokemon_name_translations.csv')
    # print(file_path)

    with open(file_path, 'w+', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'name_eng', 'name_jp_kana'
        ])
        writer.writeheader()
        for row in pokemon_translation_data:
            writer.writerow(row)

    print("Finished writing pokemon_name_translations.csv")

except requests.exceptions.RequestException as e:
    print(e)

finally:
    time.sleep(10)  # to prevent IP ban if script gets spammed somehow
