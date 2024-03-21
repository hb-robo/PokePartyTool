from bs4 import BeautifulSoup
import requests
import time
import csv
import os

"""
Western Pokemon resources tend to only have CSS-styled data for Pokemon
Stadium 2 rentals. This script scrapes the data from Serebii, transforms it,
and then stores it in a more readily workable CSV format. Japanese resources
have their versions more thoroughly catalogued, so this method is unnecessary
for those games.
"""

# Pokemon Stadium 2 Rentals
STADIUM2_URIS = {
    'little_cup': 'https://www.serebii.net/stadium2/littlerental.shtml',
    'level50': 'https://www.serebii.net/stadium2/l50rental.shtml',
    'level100': 'https://www.serebii.net/stadium2/l100rental.shtml',
}

for cup, uri in STADIUM2_URIS.items():
    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the 'table.poketab' which contain the rental Pokemon data
    elements = soup.find_all('table', class_='poketab')

    rental_data_list = []
    for element in elements:
        pokemon_data = {}

        # grab isolated data in div.poketab
        pokemon_data['Index'] = element.find('font').text.strip().split(' ')[0]
        pokemon_data['Name'] = element.find_all('tr')[1].find_all('td')[0]\
            .find(class_='label').text.strip()
        pokemon_data['Level'] = element.find_all('tr')[1].find_all('td')[0]\
            .table.find_all('tr')[2].td.text.strip().split(' ')[1]

        # collect and clean pokemon stats
        for e in element.find_all(class_='detailhead'):
            pokemon_data[e.text.strip(':')] = e.next_sibling.text

        # collect and transform pokemon movepools
        movelist = [a.text for a in element.find_all('a') if a.text != '']
        for i in range(len(movelist)):
            pokemon_data[f'Move{i+1}'] = movelist[i]

        # print(pokemon_data)
        rental_data_list.append(pokemon_data)

    script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(
        script_dir,
        f'../../data/csv/gen2/pokemon_stadium2/{cup}_rentals.csv'
    )
    # print(file_path)

    fieldnames = list(rental_data_list[0].keys()) if rental_data_list else []
    with open(file_path, 'w+', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for pokemon_data in rental_data_list:
            writer.writerow(pokemon_data)

    print(f"Finished writing {cup}_rentals.csv")
    time.sleep(10)
