import os
import sys
import json
import sqlite3
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

    def logging(
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
    logger.logging(f"Extracting data from {url}", "INFO")
    
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
            region = region_df[region_df['Country'] == cols[0]]['Region'].values[0] if cols[0] in region_df['Country'].values else 'N/A'                                     
            data[cols[0]] = cols[1:] + [region]
        logger.logging(f"Finished extracting data from {url}", "INFO")

        with open(json_path, 'w') as f:
            json.dump(data, f)
        logger.logging(f"Data is saved as {json_path}", "INFO")

    except Exception as e:
        logger.logging("Failed to extract data from Wikipedia", "ERROR")
        print(e)
        success_flag = False

    return success_flag


def transform_to_dbtable(
    json_path: str | os.PathLike,
    db_path: str | os.PathLike,
    logger: Logger,
) -> bool:
    """Transform Data to database table
    
    Args:
        json_path (str | os.PathLike): JSON filepath
        db_path (str | os.PathLike): Database filepath
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    success_flag = True
    logger.logging("Transforming data", "INFO")
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # check db file exists
        if os.path.exists(db_path):
            return success_flag

        # Create Database
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE WorldEconomies (
                Country TEXT PRIMARY KEY,
                GDP FLOAT,
                Year FLOAT,
                Region TEXT
            )            
        """)
        conn.commit()
        
        # INSERT data into Database(world_economies)
        for country, values in data.items():
            gdp, year, region = values[0], values[1], values[-1]
            if gdp == '—':
                conn.execute(
                    "INSERT INTO WorldEconomies (Country) VALUES (?)",
                    (country, )
                )
            else:
                gdp = float(gdp.replace(',', ''))
                gdp = round(gdp*0.001, 2) # million to billion
                if len(year) > 4:
                    year = int(year[-4:])
                conn.execute(
                    "INSERT INTO WorldEconomies VALUES (?, ?, ?, ?)",
                    (country, gdp, year, region)
                )
        conn.commit()
        logger.logging(f"DB Table is saved as {db_path}", "INFO")

    except Exception as e:
        logger.logging("Failed to transform data", "ERROR")
        print(e)
        success_flag = False
        os.remove(db_path)
        
    return success_flag   


def load(
    db_path: str | os.PathLike,
    logger: Logger,
)-> None:
    """Load Database and print results
    
    Args:
        db_path (str | os.PathLike): Database filepath
        logger (Logger): Logger
    Returns:
        None
    """
    
    logger.logging("Loading data", "INFO")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Print Countries with GDP over 100 billion USD
    cursor.execute("""
        SELECT * 
        FROM WorldEconomies
        WHERE GDP >= 100;
    """)
    
    print("Countries with GDP over 100 billion USD with SQL:")
    for row in cursor.fetchall():
        print(row)
    
    # Print Average GDP of top 5 countries in each region
    cursor.execute("""
        WITH Top5 AS (
            SELECT 
                Country, 
                GDP, 
                Region,
                ROW_NUMBER() OVER(PARTITION BY Region ORDER BY GDP DESC) AS rnk
            FROM WorldEconomies
            WHERE GDP IS NOT NULL
        )
        SELECT Region, AVG(GDP) AS Top5_AVG_GDP 
        FROM Top5
        WHERE rnk <= 5
        GROUP BY Region
    """)
    
    print("\nAverage GDP of top 5 countries in each region:")
    for row in cursor.fetchall():
        print(row)
    conn.close()
    
    logger.logging("Data is loaded", "INFO")
    

if __name__ == '__main__':
    LOGGER_PATH = "etl_project_log.txt"
    RAW_TXT_PATH = "region.txt"
    REGION_DF_PATH = "region.csv"
    WIKI_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    JSON_PATH = "Countries_by_GDP.json"
    DB_PATH = "Countries_by_GDP.db"

    logger = Logger(LOGGER_PATH)
    logger.logging("ETL Process is Started", "INFO")
    
    make_region_df(RAW_TXT_PATH, REGION_DF_PATH)
    ext_flag = extract(WIKI_URL, REGION_DF_PATH, JSON_PATH, logger)
    if not ext_flag:
        sys.exit(0)

    trf_flag = transform_to_dbtable(JSON_PATH, DB_PATH, logger)
    if not trf_flag:
        sys.exit(0)

    load(DB_PATH, logger)
    logger.logging("ETL Process is Finished", "INFO")