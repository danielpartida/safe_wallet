import streamlit as st

from charts import create_line_chart, create_area_chart
from read_data import read_config_file, get_offchain_data, get_onchain_data
from utils import (create_metrics_section, create_expander_section, compute_daily_share, display_no_chains_message,
                   build_alerts_section, display_metrics_sub_header, display_charts_sub_header, read_percentage_per_chain)

# Tracking parameter
percentage_per_chain, percentage_cookies = read_percentage_per_chain()

# Reading data
config = read_config_file()
column_mapping = {str(k): v for k, v in config['chain_id'].items()}

# Onchain data
df_onchain_safes = get_onchain_data(file_path='data/dune_safes.csv', values='created_safes')
df_onchain_tx = get_onchain_data(file_path='data/dune_tx_made.csv', values='safe_txs')

# Offchain data
df_offchain_safes, series_offchain_sum_safes, df_offchain_safe_monthly_change_absolute = get_offchain_data(
    column_mapping=column_mapping, file='offchain_safes.csv')
df_offchain_tx, series_offchain_sum_tx, df_offchain_tx_monthly_change_absolute = get_offchain_data(
    column_mapping=column_mapping, file='offchain_tx_made.csv')

# Get min and max date ranges
min_safes_date = min(df_offchain_safes.index)
max_safes_date = max(df_offchain_safes.index)
min_tx_date = min(df_offchain_tx.index)
max_tx_date = max(df_offchain_tx.index)

# Calculate daily share
df_safes_share_daily, series_safes_mean, series_safes_median, df_safes_relative, df_safe_monthly_change_share = \
    compute_daily_share(df_offchain=df_offchain_safes, df_onchain=df_onchain_safes,
                        factor_per_chain=percentage_per_chain, average_factor=percentage_cookies)
df_tx_share_daily, series_tx_mean, series_tx_median, df_tx_relative, df_tx_monthly_change = compute_daily_share(
    df_offchain=df_offchain_tx, df_onchain=df_onchain_tx, factor_per_chain=percentage_per_chain,
    average_factor=percentage_cookies)

# Streamlit part
st.set_page_config(page_title='Safe{Wallet} share', page_icon='🔐', layout='wide', initial_sidebar_state='auto')

# Sidebar section
st.sidebar.title("Menu")
page = st.sidebar.radio("Select your page", ("Safes created", "tx made"))

st.title('Safe{Wallet} vs other interfaces')
default_chains = ['ethereum', 'polygon', 'arbitrum', 'optimism']

if page == "Safes created":

    chains_options = ['ethereum', 'polygon', 'arbitrum', 'optimism', 'gnosis', 'bnb', 'avalanche']
    selected_chains = st.sidebar.multiselect('Select chains', chains_options, default=default_chains)

    if not selected_chains:  # Check if list is empty
        display_no_chains_message()

    else:
        metric_type = 'creation'

        # Alerts section
        build_alerts_section(min_date=min_safes_date, max_date=max_safes_date,
                             dune_query_link="https://dune.com/queries/2604616", type_=metric_type,
                             tracking_parameter=percentage_cookies)

        # Metrics section
        display_metrics_sub_header(type_=metric_type)

        create_metrics_section(
            number_of_chains=len(selected_chains), chains_selected=selected_chains, series_share=series_safes_median,
            series_absolute=series_offchain_sum_safes, type_=metric_type,
            df_monthly_change_share=df_safe_monthly_change_share,
            df_monthly_change_absolute=df_offchain_safe_monthly_change_absolute
        )

        create_expander_section(df_relative=df_safes_relative, series_absolute=series_offchain_sum_safes,
                                df_daily=df_safes_share_daily, min_date=min_safes_date, max_date=max_safes_date,
                                percentage_cookies=percentage_cookies, type_=metric_type)

        # Charts section
        display_charts_sub_header(type_=metric_type)

        st.text('Testing update')

        fig_absolute_line_chart = create_line_chart(df=df_offchain_safes, chains=selected_chains,
                                                    title='Weekly Safes deployed via our interface', weekly=True)
        st.plotly_chart(fig_absolute_line_chart)

        fig_share_line_chart = create_line_chart(df=df_safes_share_daily, chains=selected_chains,
                                                 title='Daily Safe creation share', weekly=False)
        st.plotly_chart(fig_share_line_chart)

        fig_area_chart = create_area_chart(df=df_safes_share_daily, chains=selected_chains,
                                           title='Normalized daily Safe{Wallet} creation share')
        st.plotly_chart(fig_area_chart)

elif page == "tx made":

    chains_options = ['ethereum', 'polygon', 'arbitrum', 'optimism', 'gnosis', 'bnb']
    selected_chains = st.sidebar.multiselect('Select chains', chains_options, default=default_chains)

    if not selected_chains:  # Check if list is empty
        display_no_chains_message()

    else:
        metric_type = 'tx_made'

        # Alerts section
        build_alerts_section(min_date=min_safes_date, max_date=max_safes_date,
                             dune_query_link="https://dune.com/queries/2632388", type_=metric_type,
                             tracking_parameter=percentage_cookies)

        # Metrics section
        display_metrics_sub_header(type_=metric_type)

        create_metrics_section(
            number_of_chains=len(selected_chains), chains_selected=selected_chains, series_share=series_tx_median,
            series_absolute=series_offchain_sum_tx, type_=metric_type, df_monthly_change_share=df_tx_monthly_change,
            df_monthly_change_absolute=df_offchain_tx_monthly_change_absolute
        )

        create_expander_section(df_relative=df_tx_relative, series_absolute=series_offchain_sum_tx,
                                df_daily=df_tx_share_daily, min_date=min_tx_date, max_date=max_tx_date,
                                percentage_cookies=percentage_cookies, type_=metric_type)

        display_charts_sub_header(type_=metric_type)

        fig_absolute_line_chart = create_line_chart(df=df_offchain_tx, chains=selected_chains,
                                                    title='Weekly Safe txs via our interface', weekly=True)
        st.plotly_chart(fig_absolute_line_chart)

        fig_share_line_chart = create_line_chart(df=df_tx_share_daily, chains=selected_chains,
                                                 title='Daily Safe tx made share', weekly=False)
        st.plotly_chart(fig_share_line_chart)

        fig_area_chart = create_area_chart(df=df_tx_share_daily, chains=selected_chains,
                                           title='Normalized daily Safe{Wallet} tx made share')
        st.plotly_chart(fig_area_chart)
