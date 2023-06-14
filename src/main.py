import streamlit as st
import pandas as pd

from charts import create_line_chart, create_area_chart
from read_data import read_config_file, get_offchain_data, get_onchain_data
from utils import create_metrics_section, create_expander_section, compute_daily_share

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

min_date = min(df_offchain_safes.index)
max_date = max(df_offchain_safes.index)

# Calculate daily share
df_share_daily = compute_daily_share(df_offchain=df_offchain_safes, df_onchain=df_onchain_safes)
df_mean = df_share_daily.mean(axis=0)
df_median = df_share_daily.median(axis=0)
df_relative = pd.DataFrame(df_mean, columns=['mean'])
df_relative['median'] = df_median

# Streamlit part
st.set_page_config(page_title='Safe{Wallet} share', page_icon='🔐', layout='wide', initial_sidebar_state='auto')

# Sidebar section
st.sidebar.title("Menu")
page = st.sidebar.radio("Select your page", ("Safes created", "tx made"))

if page == "Safes created":
    st.title('Safe{Wallet} vs other interfaces')

    chains_options = ['ethereum', 'polygon', 'arbitrum', 'optimism', 'gnosis', 'avalanche', 'bnb']
    default_chains = ['ethereum', 'polygon', 'arbitrum', 'optimism']
    selected_chains = st.sidebar.multiselect('Select chains', chains_options, default=default_chains)

    if not selected_chains:  # Check if list is empty
        st.error('Please select at least one chain from the sidebar.')

    else:
        # Alerts section
        col_caption_1, col_caption_2 = st.columns(2)
        col_caption_1.caption('🚨 Data fetched from **{0}** to **{1}** 🚨'.format(min_date.strftime('%d-%m-%Y'),
                                                                                max_date.strftime('%d-%m-%Y')))
        col_caption_2.caption('🚨 We assume **80%** of users accept web tracking 🚨')

        # Metrics section
        st.subheader(body='Metrics of Safe{Wallet} share creation',
                     help='Google Analytics and Dune data as proxies')

        median = df_median.loc[selected_chains].median()
        average = df_mean.loc[selected_chains].median()

        col_median, col_avg = st.columns(2)
        col_median.metric("Median Safe{Wallet} share crosschain", '{0:.2f}%'.format(100 * median))
        col_avg.metric("Average Safe{Wallet} share crosschain", '{0:.2f}%'.format(100 * average))

        create_metrics_section(number_of_chains=len(selected_chains), chains_selected=selected_chains,
                               df=df_median, series_absolute=series_offchain_sum_safes, median=median)

        create_expander_section(df_relative=df_relative, series_absolute=series_offchain_sum_safes, df_daily=df_share_daily,
                                min_date=min_date, max_date=max_date)

        # Charts section
        st.subheader(body='Charts Safe{Wallet} share creation')

        fig_line_chart = create_line_chart(df=df_share_daily, chains=selected_chains, title='Daily Safe creation share')
        st.plotly_chart(fig_line_chart)

        fig_area_chart = create_area_chart(df=df_share_daily, chains=selected_chains,
                                           title='Normalized daily Safe{Wallet} creation share')
        st.plotly_chart(fig_area_chart)

elif page == "tx made":
    st.title('Transactions made')
    # Fill this section with your content
