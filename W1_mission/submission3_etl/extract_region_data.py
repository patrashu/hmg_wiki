import os
import time

import requests
import pandas as pd

from bs4 import BeautifulSoup as bs


# for extract region data
gdp_country_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
base_url = "https://en.wikipedia.org/wiki/"
region_df_path = 'region.csv'


def extract_region_data() -> None:
    # extract
    html = requests.get(gdp_country_url)
    soup = bs(html.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    data = {
        'Country': []
    }

    # Country/Territory: [other data]
    for i, row in enumerate(table.find_all('tr')):
        # Remove Title
        if i < 3:
            continue

        # Extract each column
        cols = [col.text.strip() for col in row.find_all(['th', 'td'])]
        data['Country'].append(cols[0])

    # rum chrome driver
    regions = {
        "Africa": "Africa", "East Africa": "Africa", "North Africa": "Africa", "Southern Africa": "Africa", "West Africa": "Africa", "Central Africa": "Africa",
        "Asia": "Asia", "Central Asia": "Asia", "East Asia": "Asia", "North Asia": "Asia", "South Asia": "Asia", "Southeast Asia": "Asia", "West Asia": "Asia",
        "Europe": "Europe", "Eastern Europe": "Europe", "Northern Europe": "Europe", "Southern Europe": "Europe", "Southeast Europe": "Europe", "Western Europe": "Europe",
        "Western Europe": "Europe", "Central Europe": "Europe", "North America": "America", "Caribbean": "America", "Central America": "America", "America": "America",
        "Oceania": "Oceania", "Australia": "Oceania", "Melanesia": "Oceania", "Micronesia": "Oceania", "Polynesia": "Oceania", "China": "Asia", 'British': 'Europe',
        'West Indies': "America", "France": "Europe", "Florida": "America", "Adriatic": "Europe", 'southeast': "Europe"
    }

    data['Country'].append("Montenegro")
    country_to_region = {}
    for country in data['Country']:
        try:
            country: str = country.replace(' ', '_')
            for aux_url in ['', '_(region)', '_(country)']:
                search_url = base_url + country + aux_url
                try:
                    html = requests.get(search_url)
                    soup = bs(html.content, 'html.parser')
                    main_contents = soup.find(
                        'div', {'class': 'mw-content-ltr mw-parser-output'})
                    paragraphs = main_contents.find_all('p')
                    if not paragraphs:
                        continue
                    break
                except:
                    continue

            for idx in range(1, 5):
                f_paragraph = paragraphs[idx].text.split('. ')
                if len(f_paragraph) < 2:
                    continue

                # 본문일 때
                flag = False
                for paragraph in f_paragraph:
                    for key, value in regions.items():
                        if key in paragraph:
                            country_to_region[country.replace(
                                '_', ' ')] = value
                            flag = True
                            break
                    if flag:
                        break

                if not flag:
                    country_to_region[country.replace('_', ' ')] = 'None'
                break

        except Exception as e:
            pass

    # save to csv
    df = pd.DataFrame(data=country_to_region.items(),
                      columns=['Country', 'Region'])
    df.to_csv(region_df_path, index=False)


# Processing time: 153 seconds
if __name__ == '__main__':
    # auto extract to dataframe
    s_time = time.time()
    extract_region_data()
    e_time = time.time()
    print(f"Done! {e_time - s_time:.2f} sec")
