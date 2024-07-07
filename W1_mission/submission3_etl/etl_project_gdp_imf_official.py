import os
import sys
import time
import json
import sqlite3
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


LOGGER_PATH = "etl_project_log.txt"
YEAR = 2024
IMF_URL = f"https://www.imf.org/external/datamapper/NGDPD@WEO/OEMDC/ADVEC/WEOWORLD?year={YEAR}"
REGION_DF_PATH = "region.csv"
JSON_PATH = "imf_official.json"
DB_PATH = "imf_official.db"


class Logger:
    """Logger Class"""

    def __init__(self, log_file: str | os.PathLike) -> None:
        """__init__ Constructor

        Args
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


def extract(
    url: str,
    year: int,
    logger: Logger
) -> dict:
    """Extract Table Data from Wikipedia

    Args:
        url (str): Wikipedia URL
        region_df_path (str, os.PathLike): Region DataFrame filepath
        year (int): Year
        json_path (str, os.PathLike): JSON filepath to save
        logger (Logger): Logger
    Returns:
        data (dict): Extracted Data
    """
    logger.log(f"Extracting starte !!", "INFO")

    try:
        # set driver
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        # get data
        driver.get(url)
        time.sleep(20)

        data = {
            'Country': [],
            'GDP': [],
            'Year': [],
        }
        i = 1
        while True:
            try:
                xpath = f'//*[@id="dm-main"]/div[1]/radio-group/div[3]/imf-ranking/radio-group/div[2]/div[2]/div[{i}]/div'
                country, gdp = driver.find_element(
                    By.XPATH, xpath).text.split('\n')
                data['Country'].append(country)
                data['GDP'].append(gdp)
                data['Year'].append(year)
                i += 1
            except:
                break

        driver.quit()
        return data

    except Exception as e:
        logger.log("Extracting Failed", "ERROR")
        print(e)
        sys.exit(0)


def transform(
    json_data: dict,
    region_df_path: pd.DataFrame,
    logger: Logger,
) -> pd.DataFrame:
    """Transform Data

    Args:
        json_path (json_data): JSON filepath
        region_df_path (pd.DataFrame): Region DataFrame filepath
        logger (Logger): Logger
    Returns:
        df (pd.DataFrame): DataFrame
    """

    def raw_value_to_str_format(x: str):
        if x == 'no data':
            return '0'
        x = x.split()
        if len(x) == 1:
            return x[0]
        elif x[1] == 'thousand':
            return str(float(x[0]) * 1000)
        else:
            raise ValueError(f"Unknown value: {x}")

    logger.log("Transforming Start !!")
    try:
        df = pd.DataFrame(json_data)
        region_df = pd.read_csv(region_df_path)

        df['GDP_USD_B'] = df['GDP'].apply(raw_value_to_str_format)
        df['GDP_USD_B'] = df['GDP_USD_B'].round(2)

        df = pd.merge(df, region_df, on='Country', how='left')
        logger.log("Transforming Finished !!")

        return df

    except Exception as e:
        logger.log("Transforming Failed", "ERROR")
        print(e)
        sys.exit(0)


def load(
    df: pd.DataFrame,
    db_path: str | os.PathLike,
    year: int,
    logger: Logger,
) -> None:
    """Save Transformed Data to DB Table

    Args:
        df (pd.DataFrame): DataFrame
        db_path (str | os.PathLike): Database filepath
        year (int): Year
        logger (Logger): Logger
    Returns:
        None
    """
    logger.log("Loading Start !!")
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create Database
    conn = sqlite3.connect(db_path)
    conn.execute(f"""
        CREATE TABLE WorldEconomies_{year} (
            Country TEXT PRIMARY KEY,
            GDP FLOAT,
            Region TEXT
        )            
    """)
    conn.commit()

    # INSERT data into Database(world_economies)
    for _, row in df.iterrows():
        conn.execute(
            f"INSERT INTO WorldEconomies_{year} VALUES (?, ?, ?)",
            (row['Country'], row['GDP_USD_B'], row['Region'])
        )
    conn.commit()
    conn.close()
    logger.log("Logging Finished !!")


def query_gdp_over_usd_100b(
    db_path: str | os.PathLike,
    year: int,
    logger: Logger,
) -> None:
    """Query GDP over USD 100B"""
    logger.log("Query GDP over USD 100B", "INFO")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT * 
        FROM WorldEconomies_{year}
        WHERE GDP >= 100
        ORDER BY GDP DESC;
    """)

    print("Countries with GDP over 100 billion USD with SQL:")
    for row in cursor.fetchall():
        print(row)

    logger.log("Querying Finished !!", "INFO")
    conn.close()


def query_top5_mean_per_region(
    db_path: str | os.PathLike,
    year: int,
    logger: Logger,
) -> None:
    """Query top5 mean value of GDP per region"""
    logger.log("Querying top5 mean value of GDP per region", "INFO")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        WITH Top5 AS (
            SELECT 
                Country, 
                GDP, 
                Region,
                ROW_NUMBER() OVER(PARTITION BY Region ORDER BY GDP DESC) AS rnk
            FROM WorldEconomies_{year}
            WHERE GDP IS NOT NULL
        )
        SELECT Region, AVG(GDP) AS Top5_AVG_GDP 
        FROM Top5
        WHERE rnk <= 5
        GROUP BY Region
        ORDER BY Top5_AVG_GDP DESC;
    """)

    print("\nAverage GDP of top 5 countries in each region:")
    for row in cursor.fetchall():
        print(row)

    logger.log("Querying Finished !!", "INFO")
    conn.close()


if __name__ == '__main__':
    logger = Logger(LOGGER_PATH)
    logger.log("ETL Process Started", "INFO")

    extract_data = extract(IMF_URL, YEAR, logger)
    transform_data = transform(extract_data, REGION_DF_PATH, logger)
    load(transform_data, DB_PATH, YEAR, logger)
    query_gdp_over_usd_100b(DB_PATH, YEAR, logger)
    query_top5_mean_per_region(DB_PATH, YEAR, logger)

    logger.log("ETL Process is Finished", "INFO")
