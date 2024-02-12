'''
Python Project - Scrape Countries Population Data From an HTML Table into CSV and Excel Using Python
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.worldometers.info/world-population/population-by-country/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find('table', {'id': 'example2'}).find('tbody').find_all('tr')

countries_list = []

for row in rows:
    dic = {}

    dic['Country'] = row.find_all('td')[1].text
    dic['Population (2023)'] = row.find_all('td')[2].text.replace(',', '')
    dic['Yearly  Change'] = row.find_all('td')[3].text
    dic['Net  Change'] = row.find_all('td')[4].text
    dic['Density (P/Km²)'] = row.find_all('td')[5].text
    dic['Land Area (Km²)'] = row.find_all('td')[6].text
    dic['Migrants (net)'] = row.find_all('td')[7].text
    dic['Fert. Rate'] = row.find_all('td')[8].text
    dic['Med. Age'] = row.find_all('td')[9].text
    dic['Urban Pop %'] = row.find_all('td')[10].text
    dic['World Share'] = row.find_all('td')[11].text

    countries_list.append(dic)

df = pd.DataFrame(countries_list)
df.to_excel('countries_data.xlsx', index=False)
df.to_csv('countries_data.csv', index=False)

print("\nData Saved Successfully :)\n")
