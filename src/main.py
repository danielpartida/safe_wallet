import streamlit as st

from charts import create_line_chart, create_area_chart
from read_data import read_config_file, get_offchain_data, get_onchain_data
from utils import (create_metrics_section, create_expander_section, compute_daily_share, display_no_chains_message,
                   build_alerts_section, display_metrics_subheader)

# Reading data
config = read_config_file()
column_mapping = {str(k): v for k, v in config['chain_id'].items()}

# Onchain data
df_onchain_safes = get_onchain_data(file_path='data/dune_safes.csv', values='created_safes')
df_onchain_tx = get_onchain_data(file_path='data/dune_tx_made.csv', values='safe_txs')

# Offchain data
df_offchain_safes, series_offchain_sum_safes = get_offchain_data(column_mapping=column_mapping,
                                                                 file='offchain_safes.csv')
df_offchain_tx, series_offchain_sum_tx = get_offchain_data(column_mapping=column_mapping, file='offchain_tx_made.csv')

# Get min and max date ranges
min_safes_date = min(df_offchain_safes.index)
max_safes_date = max(df_offchain_safes.index)
min_tx_date = min(df_offchain_tx.index)
max_tx_date = max(df_offchain_tx.index)

# Calculate daily share
df_safes_share_daily, series_safes_mean, series_safes_median, df_safes_relative = compute_daily_share(
    df_offchain=df_offchain_safes, df_onchain=df_onchain_safes)
df_tx_share_daily, series_tx_mean, series_tx_median, df_tx_relative = compute_daily_share(
    df_offchain=df_offchain_tx, df_onchain=df_onchain_tx)

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
        # Alerts section
        build_alerts_section(min_date=min_safes_date, max_date=max_safes_date)

        # Metrics section
        metric_type = 'creation'
        display_metrics_subheader(type=metric_type)

        create_metrics_section(
            number_of_chains=len(selected_chains), chains_selected=selected_chains, series_median=series_safes_median,
            series_mean=series_safes_mean, series_absolute=series_offchain_sum_safes)

        create_expander_section(df_relative=df_safes_relative, series_absolute=series_offchain_sum_safes,
                                df_daily=df_safes_share_daily, min_date=min_safes_date, max_date=max_safes_date)

        # Charts section
        st.subheader(body='Charts Safe{Wallet} share creation')

        fig_line_chart = create_line_chart(df=df_safes_share_daily, chains=selected_chains,
                                           title='Daily Safe creation share')
        st.plotly_chart(fig_line_chart)

        fig_area_chart = create_area_chart(df=df_safes_share_daily, chains=selected_chains,
                                           title='Normalized daily Safe{Wallet} creation share')
        st.plotly_chart(fig_area_chart)

elif page == "tx made":

    chains_options = ['ethereum', 'polygon', 'arbitrum', 'optimism', 'gnosis', 'bnb']
    selected_chains = st.sidebar.multiselect('Select chains', chains_options, default=default_chains)

    if not selected_chains:  # Check if list is empty
        display_no_chains_message()

    else:
        # Alerts section
        build_alerts_section(min_date=min_safes_date, max_date=max_safes_date)

        # Metrics section
        metric_type = 'tx_made'
        display_metrics_subheader(type=metric_type)

        create_metrics_section(
            number_of_chains=len(selected_chains), chains_selected=selected_chains, series_median=series_tx_median,
            series_mean=series_tx_mean, series_absolute=series_offchain_sum_tx)

        create_expander_section(df_relative=df_tx_relative, series_absolute=series_offchain_sum_tx,
                                df_daily=df_tx_share_daily, min_date=min_tx_date, max_date=max_tx_date)
        