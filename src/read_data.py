from typing import Tuple

import yaml
import pandas as pd


def read_config_file(filepath: str = 'data/config.yml'):
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_offchain_data(column_mapping: dict, file: str, path: str = 'data/') -> Tuple[pd.DataFrame, pd.Series]:
    file_path = path + file
    df = pd.read_csv(file_path, index_col='date')

    if bool(column_mapping):
        df.rename(columns=column_mapping, inplace=True)

    df.index = pd.to_datetime(df.index, format='%Y%m%d')

    return df, df.sum(axis=0)


def get_onchain_data(file_path: str, values: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df.pivot(index='date', columns='blockchain', values=values)

    # If there are any NaN values you might want to fill them with a suitable value, e.g., 0
    df.fillna(0, inplace=True)

    if file_path == 'data/dune_safes.csv':
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    else:
        df.index = pd.to_datetime(df.index)
        df.index = df.index.date
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

    df.rename(columns={'avalanche_c': 'avalanche'}, inplace=True)

    return df
