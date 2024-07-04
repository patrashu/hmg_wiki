import os
import sys
import time
import json
import sqlite3
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


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


def extract_imf_official(
    url: str,
    region_df_path: str | os.PathLike,
    year: int,
    json_path: str | os.PathLike,
    logger: Logger
):
    """Extract Table Data from Wikipedia and Save as JSON
    
    Args:
        url (str): Wikipedia URL
        region_df_path (str, os.PathLike): Region DataFrame filepath
        year (int): Year
        json_path (str, os.PathLike): JSON filepath to save
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    
    success_flag = True
    logger.log(f"Extracting data from IMF Official: {url}")
    region_df = pd.read_csv(region_df_path)
    
    try:
        # set driver
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        
        # get data
        driver.get(url)
        time.sleep(20)
        
        data = {}
        i = 1
        while True:
            try:
                xpath = f'//*[@id="dm-main"]/div[1]/radio-group/div[3]/imf-ranking/radio-group/div[2]/div[2]/div[{i}]/div'
                country, gdp = driver.find_element(By.XPATH, xpath).text.split('\n')
                if gdp == 'no data':
                    pass
                else:
                    gdp = gdp.split()
                    if len(gdp) == 1:
                        gdp = float(gdp[0])
                    else:
                        gdp = float(gdp[0]) * 1000
                    
                    # get region of the country
                    region = None
                    try:
                        region = region_df[region_df["Country"] == country]["Region"].values[0]
                    except:
                        tmp = None
                        for coun in region_df["Country"]:
                            if coun in country:
                                tmp = coun
                                break
                        if tmp:
                            region = region_df[region_df["Country"] == tmp]["Region"].values[0]
                        else:
                            region = "Unknown"
                    finally:
                        data[country] = [gdp, year, region]
                i += 1
            except:
                break

        driver.quit()
        logger.log("Data Extracted Successfully", "INFO")
        
        with open(str(year) + json_path, 'w') as f:
            json.dump(data, f)
        logger.log(f"Data is saved as {json_path}", "INFO")
            
    except Exception as e:
        logger.log("Failed to extract data from IMF Official", "ERROR")
        print(e)
        success_flag = False

    return success_flag
    
    
def transform_to_dbtable(
    json_path: str | os.PathLike,
    year: int,
    db_path: str | os.PathLike,
    logger: Logger
) -> bool:
    """Transform JSON Data to Database Table
    
    Args:
        json_path (str | os.PathLike): JSON filepath
        year (int): Year
        db_path (str | os.PathLike): Database filepath
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    
    success_flag = True
    logger.log("Transforming JSON Data to Database Table", "INFO")
    try:
        json_path = str(year) + json_path
        db_path = str(year) + db_path
        
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
                Year TEXT,
                Region TEXT
            )            
        """)
        conn.commit()
        
        # INSERT data into Database(world_economies)
        for country, values in data.items():
            gdp, year, region = values[0], values[1], values[-1]
            if gdp == '—':
                continue
            gdp = round(gdp, 2) # million to billion
            conn.execute(
                "INSERT INTO WorldEconomies VALUES (?, ?, ?, ?)",
                (country, gdp, year, region)
            )
        conn.commit()
        logger.log(f"DB Table is saved as {db_path}", "INFO")
    
    except Exception as e:
        logger.log("Failed to transform data", "ERROR")
        print(e)
        success_flag = False
        os.remove(db_path)
   
    return success_flag


def load(
    db_path: str | os.PathLike,
    year: int,
    logger: Logger
) -> bool:
    """Load Data from Database
    
    Args:
        db_path (str | os.PathLike): Database filepath
        yead (int): Year
        logger (Logger): Logger
    Returns:
        success_flag (bool): Success Flag
    """
    success_flag = True
    logger.log("Loading Data from Database", "INFO")
    try:
        db_path = str(year) + db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Print Countries with GDP over 100 billion USD
        cursor.execute("""
            SELECT * 
            FROM WorldEconomies
            WHERE GDP >= 100
            ORDER BY GDP DESC;
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
            ORDER BY Top5_AVG_GDP DESC;
        """)
        
        print("\nAverage GDP of top 5 countries in each region:")
        for row in cursor.fetchall():
            print(row)
        conn.close()
        
        logger.log("All Queries are Finished", "INFO")
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
    YEAR = 2024
    IMF_URL = f"https://www.imf.org/external/datamapper/NGDPD@WEO/OEMDC/ADVEC/WEOWORLD?year={YEAR}"
    JSON_PATH = "imf_official.json"
    DB_PATH = "imf_official.db"
    
    logger = Logger(LOGGER_PATH)
    logger.log("ETL Process Started", "INFO")
    
    make_region_df(RAW_TXT_PATH, REGION_DF_PATH)
    ext_flag = extract_imf_official(IMF_URL, REGION_DF_PATH, YEAR, JSON_PATH, logger)
    if not ext_flag:
        sys.exit(0)

    trf_flag = transform_to_dbtable(JSON_PATH, YEAR, DB_PATH, logger)
    if not trf_flag:
        sys.exit(0)

    load_flag = load(DB_PATH, YEAR, logger)
    if not load_flag:
        sys.exit(0)
    logger.log("ETL Process is Finished", "INFO")