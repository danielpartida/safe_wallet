import pandas as pd
import streamlit as st


# TODO: Add monthly change to absolute numbers
def create_metrics_section(number_of_chains: int, chains_selected: list, df: pd.DataFrame,
                           series_absolute: pd.Series, median: float):

    cols = st.columns(number_of_chains)
    for i, chain in enumerate(chains_selected):
        if chain not in df.index or chain not in series_absolute.index:
            st.error("Chain {0} not found in data".format(chain))
            continue

        # Metrics for current chain
        chain_share = df.loc[chain, 'median']
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
