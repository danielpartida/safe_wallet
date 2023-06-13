import pandas as pd
import plotly.graph_objects as go


def create_line_chart(df: pd.DataFrame, columns: list, title: str) -> go.Figure:
    fig = go.Figure()

    for column in columns:
        fig.add_trace(go.Scatter(x=df.date, y=df[column], mode='lines', name=column))

    fig.update_layout(
        title=title,
        showlegend=True
    )

    return fig
