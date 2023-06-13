import yaml
import pandas as pd


def read_config_file(filepath: str = 'data/config.yaml'):
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_offchain_tx(column_mapping: dict, file_path: str = 'data/offchain_tx_made.csv') -> pd.DataFrame:
    df = pd.read_csv(file_path, index_col='date')
    df.rename(columns=column_mapping, inplace=True)

    return df


def get_offchain_safes(file_path: str = 'data/offchain_safes.csv') -> pd.DataFrame:
    df = pd.read_csv(file_path, index_col='date')

    return df
