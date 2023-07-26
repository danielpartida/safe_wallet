from datetime import datetime, date
from typing import Tuple

import pandas as pd
import numpy as np
import streamlit as st


def create_metrics_section(number_of_chains: int, chains_selected: list, series_median: pd.Series,
                           series_absolute: pd.Series, type_: str, df_monthly_change: pd.DataFrame):

    # General metrics subsection
    median_metric = series_median.loc[chains_selected].median()
    monthly_change = df_monthly_change.loc[:, chains_selected].median(axis=1)[-1]
    st.metric("SafeWallet share {0} crosschain".format(type_), '{0:.2f}%'.format(100 * median_metric),
              '{0:.2f}%'.format(100 * monthly_change))
    # st.caption("Median used as metric for calculation")

    cols = st.columns(number_of_chains)
    for i, chain in enumerate(chains_selected):
        if chain not in series_median.index or chain not in series_absolute.index:
            st.error("Chain {0} not found in data".format(chain))
            continue

        # Metrics for current chain
        chain_share = series_median.loc[chain]
        chain_safes = series_absolute.loc[chain]

        short_names = {
            'ethereum': 'ETH', 'polygon': 'MATIC', 'arbitrum': 'ARB', 'optimism': 'OP', "gnosis": 'GNO',
            'bnb': 'BNB', 'avalanche': 'AVAX'
        }

        # Detailed metrics subsection
        cols[i].metric("{0} SafeWallet {1} share".format(short_names[chain], type_),
                       "{0:.2f}%".format(100 * chain_share), "{0:.2f}%".format(100 * (chain_share - median_metric)))

        if type_ == 'creation':
            cols[i].metric("{0} SafeWallet Safes".format(short_names[chain]), chain_safes)

        elif type_ == 'tx_made':
            cols[i].metric("{0} SafeWallet tx made".format(short_names[chain]), chain_safes)

        else:
            cols[i].error("No metric type found")


def create_expander_section(df_relative: pd.DataFrame, series_absolute: pd.Series, df_daily: pd.DataFrame,
                            min_date: datetime, max_date: datetime, percentage_cookies: float, type_: str):
    with st.expander("See more chain metrics"):
        tab_relative, tab_absolute, tab_daily = st.tabs(["Relative metrics", "Absolute metrics", "Daily share"])

        tab_relative.text(body='Average and median Safe {0} share per chain'.format(type_))
        tab_relative.dataframe(data=df_relative)

        tab_absolute.text(body='Absolute number of Safe {0} per chain from {1} to {2}'.format(
            type_, min_date.strftime('%d-%m-%Y'), max_date.strftime('%d-%m-%Y')))
        tab_absolute.dataframe(data=pd.DataFrame(series_absolute, columns=['safes']))

        tab_daily.text(body='Data daily Safe {0} share'.format(type_))
        tab_daily.dataframe(data=df_daily)
        tab_daily.caption(
            body='Note: {0:.2f}%% of people accept tracking on web. Hence, we scale the Google Analytics data'.format(
                percentage_cookies
            )
        )


def compute_daily_share(df_offchain: pd.DataFrame, df_onchain: pd.DataFrame, factor_per_chain: pd.Series,
                        average_factor: float) -> \
        Tuple[pd.DataFrame, pd.Series, pd.Series, pd.DataFrame, pd.DataFrame]:

    df_offchain_factor = df_offchain.div(factor_per_chain, axis='columns')
    missing_columns = set(df_offchain.columns) - set(factor_per_chain.index)

    for column in missing_columns:
        df_offchain_factor[column] = df_offchain[column] / average_factor

    onchain_cols = set(df_onchain.columns)
    offchain_cols = set(df_offchain_factor.columns)

    common_cols = list(onchain_cols.intersection(offchain_cols))

    df_share = df_offchain_factor[common_cols].div(df_onchain[common_cols])
    df_share = df_share.round(2)
    df_share.index = df_share.index.date
    df_share.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_share.dropna(inplace=True)

    series_mean = df_share.mean(axis=0)
    series_median = df_share.median(axis=0)

    df_relative = pd.DataFrame(series_mean, columns=['mean'])
    df_relative['median'] = series_median

    # Compute the monthly percentage change
    df_share.index = pd.to_datetime(df_share.index)
    df_monthly_median = df_share.resample('M').median()
    df_monthly_change = df_monthly_median.pct_change()

    return df_share, series_mean, series_median, df_relative, df_monthly_change


def display_no_chains_message() -> st.error:
    return st.error('Please select at least one chain from the sidebar.')


def build_alerts_section(min_date: date, max_date: date, dune_query_link: str, type_: str,
                         tracking_parameter: float = 0.8):
    col_caption_1, col_caption_2 = st.columns(2)

    message_dates = '🚨 Data fetched from **{0}** to **{1}** 🚨'.format(
        min_date.strftime('%d-%m-%Y'), max_date.strftime('%d-%m-%Y')
    )
    col_caption_1.caption(message_dates)

    message_tracking = '🚨 We assume **{0:.2f}%** of users accept web tracking 🚨'.format(tracking_parameter*100)
    col_caption_2.caption(message_tracking)

    google_analytics_link = 'https://analytics.google.com/analytics/web/#/analysis/p308247657/edit/K8gMuB_rR9S7iXz0JhhJ_w'
    col_caption_1.caption("[Google Analytics link](%s)" % google_analytics_link)
    col_caption_2.caption("[Dune {0} link query](%s)".format(type_) % dune_query_link)


def display_metrics_sub_header(type_: str) -> st.subheader:
    return st.subheader(body='Metrics of SafeWallet share {0}'.format(type_),
                        help='Google Analytics and Dune data as proxies')


def display_charts_sub_header(type_: str) -> st.subheader:
    return st.subheader(body='Charts SafeWallet share {0}'.format(type_))


def read_percentage_per_chain() -> Tuple[pd.Series, float]:
    data = pd.read_csv('data/redefine_percentage_cookies.csv', index_col='chain_name')
    data.rename(columns={'mainnet': 'ethereum'}, inplace=True)

    data['% of users accepting tracking'] = data['% of users accepting tracking'].str.rstrip('%').astype(float) / 100

    cookies_average = float(data['all'].iloc[0].rstrip('%')) / 100

    return data['% of users accepting tracking'], cookies_average
