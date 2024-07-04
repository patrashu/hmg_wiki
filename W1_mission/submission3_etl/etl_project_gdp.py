import os
import sys
import json
from datetime import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


class Logger:
    """Logger Class"""
    def __init__(self, log_file: str | os.PathLike) -> None:
        """__init__ Constructor
        
        Args:
            log_file (str | os.PathLike): _description_
        Returns:
            None
        """
        self.log_file = log_file

    def log(
        self, 
        msg: str, 
        level: str = "INFO"
    ) -> None:
        """Logging Function
        
        Args:
            msg (str): _description_
            level (str, optional): _description_. Defaults to "INFO".
        Returns:
            None
        """
        timestamp = datetime.now().strftime('%Y-%B-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            line = f"{timestamp} - {level} - {msg}\n"
            f.write(line)
            print(line)
    

def make_region_df(
    raw_txt_path: str | os.PathLike,
    region_df_path: str | os.PathLike
) -> None:
    """Make Region DataFrame
    
    Args:
        raw_txt_path (str | os.PathLike): Raw Text filepath
        region_df_path (str | os.PathLike): Region DataFrame filepath
    Returns:
        None
    """
    with open(raw_txt_path, 'r') as f:
        lines = f.readlines()
    
    data = {
        'Country': [],
        'Region': []
    }
    for line in lines:
        country, region = line.strip().split(',')
        data["Country"].append(country)
        data["Region"].append(region)

    df = pd.DataFrame(data=data)
    df.to_csv(region_df_path, index=False)
    

def extract(
    url: str,
    region_df_path: str | os.PathLike,
    json_path: str | os.PathLike,
    logger: Logger
) -> bool:
    """Extract Table Data from Wikipedia and Save as JSON
    
    Args:
        url (str): Wikipedia URL
        region_df_path (str, os.PathLike): Region DataFrame filepath
        json_path (str, os.PathLike): JSON filepath to save
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    success_flag = True
    logger.log(f"Extracting data from {url}", "INFO")
    
    region_df = pd.read_csv(region_df_path)
    try:
        html = requests.get(url)
        soup = bs(html.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})

        # Country/Territory: [other data]
        data = {}
        for i, row in enumerate(table.find_all('tr')):
            # Remove Title
            if i < 3:
                continue

            # Extract each column
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            region = region_df[region_df['Country'] == cols[0]]['Region'].values[0] if cols[0] in region_df['Country'].values else None                                             
            data[cols[0]] = cols[1:] + [region]
        logger.log(f"Finished extracting data from {url}", "INFO")

        with open(json_path, 'w') as f:
            json.dump(data, f)
        logger.log(f"Data is saved as {json_path}", "INFO")

    except Exception as e:
        logger.log("Failed to extract data from Wikipedia", "ERROR")
        print(e)
        success_flag = False

    return success_flag


def transform_to_dataframe(
    json_path: str | os.PathLike,
    df_path: str | os.PathLike,
    logger: Logger,
) -> bool:
    """Transform Data to pandas dataframe
    
    Args:
        json_path (str | os.PathLike): JSON filepath
        df_path (str | os.PathLike): DataFrame filepath
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    success_flag = True
    logger.log("Transforming JSON to Pandas Dataframe", "INFO")
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Preprocessing
        new_data = []
        for country, values in data.items():
            gdp, year, region = values[0], values[1], values[-1]
            if gdp == '—':
                continue
            gdp = float(gdp.replace(',', ''))
            gdp = round(gdp*0.001, 2) # million to billion
            if len(year) > 4:
                year = year[-4:]
            new_data.append([country, gdp, year, region])

        # Sort Valuesß
        new_data = sorted(new_data, key=lambda x: -x[1])
        df = pd.DataFrame(
            new_data,
            columns=[
                "Country/Territory",
                "GDP(US$MM)",
                "Year",
                "Region"
            ],
        )
        df.to_csv(df_path, index=False)
        logger.log(f"DataFrame is saved as {df_path}", "INFO")

    except Exception as e:
        logger.log("Failed to transform data", "ERROR")
        print(e)
        success_flag = False
                                                
    return success_flag   


def load(
    df_path: str | os.PathLike,
    logger: Logger,
) -> bool:
    """Load Dataframe and print results
    
    Args:
        df_path (str | os.PathLike): DataFrame filepath
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    
    logger.log("Loading data from Pandas Dataframe", "INFO")
    success_flag = True
    try:
        df = pd.read_csv(df_path)
    
        # mission 1
        upper_100b = df[df['GDP(US$MM)'] > 100]
        print("Countries with GDP over 100 billion USD:")
        print(upper_100b)
        
        # mission 2
        group_df = df.groupby('Region', group_keys=False).apply(
                lambda x: x.nlargest(5, 'GDP(US$MM)')['GDP(US$MM)'].mean(),
                include_groups=False
            )
        print("\nAverage GDP of top 5 countries in each region:")
        print(group_df)
        logger.log("Finished loading data", "INFO")
        logger.log('Done!!', 'INFO')
        
    except Exception as e:
        logger.log("Failed to load data", "ERROR")
        print(e)
        success_flag = False
    
    return success_flag
    

if __name__ == '__main__':
    LOGGER_PATH = "etl_project_log.txt"
    RAW_TXT_PATH = "region.txt"
    REGION_DF_PATH = "region.csv"
    WIKI_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    JSON_PATH = "Countries_by_GDP.json"
    DF_PATH = "Countries_by_GDP.csv"

    logger = Logger(LOGGER_PATH)
    logger.log("ETL Process is Started", "INFO")
    
    make_region_df(RAW_TXT_PATH, REGION_DF_PATH)
    ext_flag = extract(WIKI_URL, REGION_DF_PATH, JSON_PATH, logger)
    if not ext_flag:
        sys.exit(0)

    trf_flag = transform_to_dataframe(JSON_PATH, DF_PATH, logger)
    if not trf_flag:
        sys.exit(0)

    load_flag = load(DF_PATH, logger)
    if not load_flag:
        sys.exit(0)
        
    logger.log("ETL Process is Finished", "INFO")