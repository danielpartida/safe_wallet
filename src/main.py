import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from charts import create_line_chart

# Reading data
df_pct = pd.read_csv('data/df_pct.csv')
df_results = pd.read_csv('data/df_result.csv', index_col='chain')
df_wallet = pd.read_csv('data/offchain.csv', index_col='date')
df_wallet.index = pd.to_datetime(df_wallet.index, format='%Y%m%d')
series_wallet_absolute = df_wallet.sum(axis=0)
min_date = min(df_wallet.index)
max_date = max(df_wallet.index)

# Streamlit part
st.title('Safe{Wallet} vs other interfaces')

col_caption_1, col_caption_2 = st.columns(2)
col_caption_1.caption('🚨 Data fetched from **{0}** to **{1}** 🚨'.format(min_date.strftime('%d-%m-%Y'),
                                                                max_date.strftime('%d-%m-%Y')))

col_caption_2.caption('🚨 We assume **80%** of users accept web tracking 🚨')


st.subheader(body='Share of Safe{Wallet} creation',
             help='Google Analytics and Dune data as proxies')

chains = ['ethereum', 'polygon', 'optimism', 'arbitrum']
median = df_results.loc[chains]['median'].median()
average = df_results.loc[chains]['mean'].median()

col_median, col_avg = st.columns(2)
col_median.metric("Median Safe{Wallet} share crosschain", '{0:.2f}%'.format(100 * median))
col_avg.metric("Average Safe{Wallet} share crosschain", '{0:.2f}%'.format(100 * average))

# TODO: Add monthly change to absolute numbers
col1, col2, col3, col4 = st.columns(4)
col1.metric("ETH Safe{Wallet} share", "{0:.2f}%".format(100 * df_results['median'].ethereum),
            "{0:.2f}%".format(100 * (df_results['median'].ethereum - median)))
col1.metric("ETH Safe{Wallet} Safes", series_wallet_absolute.ethereum)

col2.metric("MATIC Safe{Wallet} share", "{0:.2f}%".format(100 * df_results['median'].polygon),
            "{0:.2f}%".format(100 * (df_results['median'].polygon - median)))
col2.metric("MATIC Safe{Wallet} Safes", series_wallet_absolute.polygon)

col3.metric("ARB Safe{Wallet} share", "{0:.2f}%".format(100 * df_results['median'].arbitrum),
            "{0:.2f}%".format(100 * (df_results['median'].arbitrum - median)))
col3.metric("ARB Safe{Wallet} Safes", series_wallet_absolute.arbitrum)

col4.metric("OP Safe{Wallet} share", "{0:.2f}%".format(100 * df_results['median'].optimism),
            "{0:.2f}%".format(100 * (df_results['median'].optimism - median)))
col4.metric("OP Safe{Wallet} Safes", series_wallet_absolute.optimism)

with st.expander("See more chain metrics"):
    tab_relative, tab_absolute = st.tabs(["Relative metrics", "Absolute metrics"])

    tab_relative.text(body='Average and median Safe creation share')
    tab_relative.dataframe(data=df_results)

    tab_absolute.text(body='Absolute numbers')
    tab_absolute.dataframe(data=pd.DataFrame(series_wallet_absolute, columns=['safes']))

fig_1 = create_line_chart(df=df_pct, columns=chains, title='Daily Safe creation share')
st.plotly_chart(fig_1)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.ethereum,
    mode='lines',
    name='ethereum',
    line=dict(width=0.5, color='grey'),
    stackgroup='one',  # define stack group
    groupnorm='percent'  # sets the normalization for the sum of the stackgroup
))
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.polygon,
    mode='lines',
    name='polygon',
    line=dict(width=0.5, color='purple'),
    stackgroup='one'
))
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.arbitrum,
    mode='lines',
    name='arbitrum',
    line=dict(width=0.5, color='blue'),
    stackgroup='one'
))
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.optimism,
    mode='lines',
    name='optimism',
    line=dict(width=0.5, color='red'),
    stackgroup='one'
))
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.gnosis,
    mode='lines',
    name='gnosis',
    line=dict(width=0.5, color='green'),
    stackgroup='one'
))
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.avalanche,
    mode='lines',
    name='avalanche',
    line=dict(width=0.5, color='orange'),
    stackgroup='one'
))
fig.update_layout(
    title='Normalized daily Safe creation % Safe{Wallet} / ecosystem',
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%')
)
st.plotly_chart(fig)

st.text(body='Data daily Safe creation share')
st.dataframe(data=df_pct, hide_index=True)
st.caption(body='Note: 80% of people accept tracking on web. Hence, we scale the Google Analytics data')
