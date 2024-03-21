"""
This script grabs tables of Type vs. Type charts. There are three charts,
one for Generation 1, one for Gens 2-5, and one for Gens 6-present.

Data sourced from Bulbapedia. If a new type interaction is ever released, this
code will break as the tables are ordered in reverse chronological order.
"""

import time
import os
import csv

import requests
from bs4 import BeautifulSoup

TYPE_CHARTS_URI = 'https://bulbapedia.bulbagarden.net/wiki/Type/Type_chart'
response = requests.get(TYPE_CHARTS_URI, timeout=5)

try:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all 'table.roundtable's, which contain per-generation translations.
    tables = soup.find_all('table', class_='roundy')
    type_chart_tables = {
        'gen1/gen1': tables[2],
        'gen2/gens2-5': tables[1],
        'gen6/gens6-9': tables[0],
    }

    for gen, table in type_chart_tables.items():
        gen_type_chart_rows = []

        rows = table.find_all('tr')
        headers = rows[1].find_all('th')
        headers_list = []
        for header in headers:
            headers_list.append(header.text.strip())
        # print(headers_list)

        for row in rows[2:-1]:
            rowheads = row.find_all('th')
            if row == rows[2]:
                offtype = rowheads[1].text.strip()
            else:
                offtype = rowheads[0].text.strip()
            rowcols = row.find_all('td')
            type_data = {
                'off_type': offtype
            }
            for i in range(len(rowcols)):
                cell_data = rowcols[i].text.strip()
                cell_data_clean = cell_data[:-1].replace('½', '0.5')
                type_data[headers_list[i]] = cell_data_clean
            gen_type_chart_rows.append(type_data)

        # print(gen_type_chart_rows)

        script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(
            script_dir,
            f'../data/csv/{gen}_type_chart.csv'
        )
        # print(file_path)

        headers_list.insert(0, 'off_type')
        with open(file_path, 'w+', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers_list)
            writer.writeheader()
            for row in gen_type_chart_rows:
                writer.writerow(row)

        print(f"Finished writing {gen}_type_chart.csv.csv")

except requests.exceptions.RequestException as e:
    print(e)

finally:
    time.sleep(10)  # to prevent IP ban if script gets spammed somehow
