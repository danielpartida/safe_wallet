import pandas as pd
import plotly.graph_objects as go


def create_line_chart(df: pd.DataFrame, chains: list, title: str) -> go.Figure:
    fig = go.Figure()

    for chain in chains:
        fig.add_trace(go.Scatter(x=df.date, y=df[chain], mode='lines', name=chain))

    fig.update_layout(
        title=title,
        showlegend=True
    )

    return fig


def create_area_chart(df: pd.DataFrame, chains: list, title: str) -> go.Figure:
    fig = go.Figure()

    for i, chain in enumerate(chains):
        if i == 0:  # if first iteration
            groupnorm_value = 'percent'  # sets the normalization for the sum of the stackgroup
        else:
            groupnorm_value = None

        fig.add_trace(go.Scatter(
            x=df.date, y=df[chain],
            mode='lines',
            name=chain,
            # line=dict(width=0.5, color='grey'),
            line=dict(width=0.5),
            stackgroup='one',  # define stack group
            groupnorm=groupnorm_value
        ))

    fig.update_layout(
        title=title,
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%')
    )

    return fig
