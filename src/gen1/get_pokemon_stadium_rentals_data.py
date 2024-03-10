from bs4 import BeautifulSoup
import requests
import time
import csv

"""
Western Pokemon resources tend to only have CSS-styled data for Pokemon Stadium rentals.
This script scrapes the data from Serebii, transforms it, and then stores it in a more 
readily workable CSV format. Japanese resources have their versions more thoroughly
catalogued, so this method is unnecessary for those games.
"""

# Pokemon Stadium Rentals
STADIUM_URIS = {
    'pika_cup': 'https://www.serebii.net/stadium/pikarental.shtml',
    'petit_cup': 'https://www.serebii.net/stadium/petitrental.shtml',
    'poke_cup': 'https://www.serebii.net/stadium/pokerental.shtml',
    'prime_cup': 'https://www.serebii.net/stadium/primerental.shtml',
    "gym_leader_castle": 'https://www.serebii.net/stadium/gymrental.shtml'
}

for cup, uri in STADIUM_URIS.items():
    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the tables with the class 'poketab' which contain the rental Pokemon data
    elements = soup.find_all('table', class_='poketab')

    rental_data_list = []
    for element in elements:
        pokemon_data = {}

        # splits all text in element into string list
        pokemon_attrs = element.find('font').text.strip()
        attrs_list = pokemon_attrs.split('\n')
        attrs_list = [x for x in attrs_list if (x != '' and x != '\t')]

        # transform and collect rental Pokemon data
        pokemon_data['Index'] = attrs_list[0].split(' ')[0]
        pokemon_data['Name'] = attrs_list[1]
        pokemon_data['Level'] = attrs_list[2].split(' ')[1]
        pokemon_data['HP'] = attrs_list[3].split(':')[1]
        pokemon_data['Attack'] = attrs_list[4].split(':')[1]
        pokemon_data['Defense'] = attrs_list[5].split(':')[1]
        pokemon_data['Special'] = attrs_list[6].split(':')[1]
        pokemon_data['Speed'] = attrs_list[7].split(':')[1]
        pokemon_data['Move1'] = attrs_list[8]
        pokemon_data['Move2'] = '' if len(attrs_list) < 10 else attrs_list[9]
        pokemon_data['Move3'] = '' if len(attrs_list) < 11 else attrs_list[10]
        pokemon_data['Move4'] = '' if len(attrs_list) < 12 else attrs_list[11]

        # print(pokemon_data)
        rental_data_list.append(pokemon_data)

    # Write the cup's rental data to CSV file
    with open(f'../../data/gen1/csv/pokemon_stadium/{cup}_rentals.csv', 'w+', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Index','Name','Level','HP','Attack','Defense','Special','Speed','Move1','Move2','Move3','Move4'])
        writer.writeheader()
        for pokemon_data in rental_data_list:
            writer.writerow(pokemon_data)

    print(f"Finished writing {cup}_rentals.csv")
    time.sleep(10)