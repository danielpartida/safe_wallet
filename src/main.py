import streamlit as st
import pandas as pd

from charts import create_line_chart, create_area_chart
from utils import create_metrics_section, create_expander_section

# Reading data
df_pct = pd.read_csv('data/df_pct.csv')
df_results = pd.read_csv('data/df_result.csv', index_col='chain')
df_wallet = pd.read_csv('data/offchain.csv', index_col='date')
df_wallet.index = pd.to_datetime(df_wallet.index, format='%Y%m%d')
series_wallet_absolute = df_wallet.sum(axis=0)
min_date = min(df_wallet.index)
max_date = max(df_wallet.index)

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

        median = df_results.loc[selected_chains]['median'].median()
        average = df_results.loc[selected_chains]['mean'].median()

        col_median, col_avg = st.columns(2)
        col_median.metric("Median Safe{Wallet} share crosschain", '{0:.2f}%'.format(100 * median))
        col_avg.metric("Average Safe{Wallet} share crosschain", '{0:.2f}%'.format(100 * average))

        create_metrics_section(number_of_chains=len(selected_chains), chains_selected=selected_chains,
                                             df=df_results, series_absolute=series_wallet_absolute, median=median)

        create_expander_section(df_relative=df_results, series_absolute=series_wallet_absolute, df_daily=df_pct,
                                min_date=min_date, max_date=max_date)

        # Charts section
        st.subheader(body='Charts Safe{Wallet} share creation')

        fig_line_chart = create_line_chart(df=df_pct, chains=selected_chains, title='Daily Safe creation share')
        st.plotly_chart(fig_line_chart)

        fig_area_chart = create_area_chart(df=df_pct, chains=selected_chains,
                                           title='Normalized daily Safe{Wallet} creation share')
        st.plotly_chart(fig_area_chart)

elif page == "tx made":
    st.title('Transactions made')
    # Fill this section with your content
