import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Reading data
df_pct = pd.read_csv('data/df_pct.csv')
df_results = pd.read_csv('data/df_result.csv')

# Streamlit part
st.title('Safe{Wallet} vs other interfaces')
st.subheader(body='Share of Safe{Wallet} creation',
             help='Google Analytics and Dune data as proxies')

median = df_results['median'].median()
average = df_results['mean'].median()

col_median, col_avg = st.columns(2)
col_median.metric("Median Safe{Wallet} creation share crosschain", '{0:.2f}%'.format(100*median))
col_avg.metric("Average Safe{Wallet} creation share crosschain", '{0:.2f}%'.format(100*average))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ethereum", "{0:.2f}%".format(100*df_results['median'].iloc[0]), "{0:.2f}%".format(100*(df_results['median'].iloc[0]-median)))
col2.metric("Polygon", "{0:.2f}%".format(100*df_results['median'].iloc[1]), "{0:.2f}%".format(100*(df_results['median'].iloc[1]-median)))
col3.metric("Arbitrum", "{0:.2f}%".format(100*df_results['median'].iloc[2]), "{0:.2f}%".format(100*(df_results['median'].iloc[2]-median)))
col4.metric("Optimism", "{0:.2f}%".format(100*df_results['median'].iloc[3]), "{0:.2f}%".format(100*(df_results['median'].iloc[3]-median)))

st.text(body='Average and median Safe creation share')
st.dataframe(data=df_results, hide_index=True)

fig_1 = create_line_chart(df=df_pct, columns=chains, title='Daily Safe creation share')
st.plotly_chart(fig_1)


fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_pct.date, y=df_pct.ethereum,
    mode='lines',
    name='ethereum',
    line=dict(width=0.5, color='grey'),
    stackgroup='one', # define stack group
    groupnorm='percent' # sets the normalization for the sum of the stackgroup
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
