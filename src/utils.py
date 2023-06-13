from datetime import datetime

import pandas as pd
import streamlit as st


# TODO: Add monthly change to absolute numbers
def create_metrics_section(number_of_chains: int, chains_selected: list, df: pd.DataFrame,
                           series_absolute: pd.Series, median: float) -> st.columns:

    cols = st.columns(number_of_chains)
    for i, chain in enumerate(chains_selected):
        if chain not in df.index or chain not in series_absolute.index:
            st.error("Chain {0} not found in data".format(chain))
            continue

        # Metrics for current chain
        chain_share = df.loc[chain]
        chain_safes = series_absolute.loc[chain]

        short_names = {
            'ethereum': 'ETH', 'polygon': 'MATIC', 'arbitrum': 'ARB', 'optimism': 'OP', "gnosis": 'GNO',
            'bnb': 'BNB', 'avalanche': 'AVAX'
        }

        # Display metrics
        cols[i].metric("{0} SafeWallet share".format(short_names[chain]), "{0:.2f}%".format(100 * chain_share),
                       "{0:.2f}%".format(100 * (chain_share - median)))
        cols[i].metric("{0} SafeWallet Safes".format(short_names[chain]), chain_safes)

    return cols


def create_expander_section(df_relative: pd.DataFrame, series_absolute: pd.Series, df_daily: pd.DataFrame,
                            min_date: datetime, max_date: datetime):
    with st.expander("See more chain metrics"):
        tab_relative, tab_absolute, tab_daily = st.tabs(["Relative metrics", "Absolute metrics", "Daily share"])

        tab_relative.text(body='Average and median Safe creation share per chain')
        tab_relative.dataframe(data=df_relative)

        tab_absolute.text(body='Absolute number of Safes deployed per chain from {0} to {1}'.format(
            min_date.strftime('%d-%m-%Y'), max_date.strftime('%d-%m-%Y')))
        tab_absolute.dataframe(data=pd.DataFrame(series_absolute, columns=['safes']))

        tab_daily.text(body='Data daily Safe creation share')
        tab_daily.dataframe(data=df_daily, hide_index=True)
        tab_daily.caption(body='Note: 80% of people accept tracking on web. Hence, we scale the Google Analytics data')


def compute_daily_share(df_offchain: pd.DataFrame, df_onchain: pd.DataFrame, factor: float = 0.8) -> pd.DataFrame:
    df_offchain /= factor

    onchain_cols = set(df_onchain.columns)
    offchain_cols = set(df_offchain.columns)

    common_cols = list(onchain_cols.intersection(offchain_cols))

    df_share = df_offchain[common_cols].div(df_onchain[common_cols])
    df_share = df_share.round(2)

    df_mean = df_share.mean(axis=0)
    df_median = df_share.median(axis=0)

    return df_share