import requests
from bs4 import BeautifulSoup
import pandas as pd

#Requests API for all data to compile a list of countries
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)

if response.status_code == 200: 
    countries_data = response.json()
    country_names = [country['name']['common'] for country in countries_data]
    country_names.sort()
else:
    print(f"Error fetching data: {response.status_code}")

#Stores data for each country in a dict
country_dict = {}

for country_name in country_names:
    country_url = f"https://restcountries.com/v3.1/name/{country_name}"
    country_response = requests.get(country_url)

    if country_response.status_code == 200:
        country_info = country_response.json()[0]   
        country_data = {
            'capital': country_info.get('capital', ['N/A'])[0],
            'population': country_info.get('population', 'N/A'),
            'area (in square km)': country_info.get('area', 'N/A'),
            'region': country_info.get('region', 'N/A'),
            'subregion': country_info.get('subregion', 'N/A'),
            'languages': list(country_info.get('languages', {}).values()),
            'currency': list(country_info.get('currencies', {}).values())[0]['name'] if country_info.get('currencies') else 'N/A',
        }
        country_dict[country_name] = country_data
    else:
        print(f"Error fetching data for {country_name}: {country_response.status_code}")

scrape_url = "https://www.bbc.com/news/country-profiles"
scrape_response = requests.get(scrape_url)

if scrape_response.status_code == 200:
    soup = BeautifulSoup(scrape_response.text, 'html.parser')
    country_profiles = soup.find_all('li', class_='ssrcss-1ltsh3x-ColumnLi ecc37rf6')
    for country_name in country_names:
        found = 0
        for profile in country_profiles:
            if country_name == profile.find('a').text.strip():
                found = 1
                new_url = profile.find('a')['href']
                if not new_url.startswith('http'):
                    new_url = f"https://www.bbc.com{new_url}"
                scrape_country = requests.get(new_url)
                if scrape_country.status_code == 200:
                    soup2 = BeautifulSoup(scrape_country.text, 'html.parser')
                    life_expectancy_data = soup2.find_all('p')
                    for paragraph in life_expectancy_data:
                        text = paragraph.get_text()
                        if "life expectancy" in text.lower():
                            data = text.split(' ')
                            country_dict[country_name]['male_life_expectancy'] = data[2]
                            country_dict[country_name]['female_life_expectancy'] = data[5]
                else:
                    print(f'Error finding webpage')
        if found == 0:
            country_dict[country_name]['male_life_expectancy'] = 'N/A'
            country_dict[country_name]['female_life_expectancy'] = 'N/A'
else:
    print(f"Error fetching data: {response.status_code}")

df = pd.DataFrame.from_dict(country_dict, orient='index')
df.reset_index(inplace=True)
df.rename(columns={'index': 'Country'}, inplace=True)
df.to_csv('countries_data.csv', index = False)

