import os
import pandas as pd


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
        'Country/Territory': [],
        'Region': []
    }
    for line in lines:
        country, region = line.strip().split(',')
        data["Country/Territory"].append(country)
        data["Region"].append(region)

    df = pd.DataFrame(data=data)
    df.to_csv(region_df_path, index=False)
    

if __name__ == '__main__':
    raw_txt_path = 'regions.txt'
    region_df_path = 'regions.csv'
    make_region_df(raw_txt_path, region_df_path)
    print("Region DataFrame Created !!")