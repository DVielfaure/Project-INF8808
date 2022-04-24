import plotly.graph_objects as go
from plotly.subplots import make_subplots

MAX_DISPLAYED_POINTS = 99999
df_col = ['Lenght', 'Width', 'DeadWeight Tonnage', 'Maximum Draugth']
x_title = ['Lenght (m)', 'Width (m)', 'DeadWeight Tonnage (kg)', "Maximum Draugth (m)"]
colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)']

def showScatter(df_size):
    return False if df_size > MAX_DISPLAYED_POINTS else 'all'


def boxplot(dataY, name, color):
    return go.Box(
        y=dataY,
        name=name,
        boxpoints=showScatter(dataY.size),
        jitter=0.3,
        whiskerwidth=0.2,
        fillcolor=color,
        marker_size=3,
        marker_opacity=0.2,
        line_width=1,
        boxmean=True,
        hoverinfo="y"
    )


def trace_boxplot(df):
    fig = make_subplots(rows=1, cols=4)

    position = 1
    for (column, xTitle, color) in zip(df_col, x_title, colors):
        fig.add_trace(boxplot(df[column], xTitle, color), row=1, col=position)
        position += 1

    fig.update_layout(
        title='Distribution of vessel characteristics',
        showlegend=False,
        title_x=0.5,
        margin=dict(l=14, r=14, t=32, b=14, pad=0),
    )

    return fig


def update_traces_boxplot(data, fig):
    position = 1
    for col in df_col:
        fig.update_traces(y=data[col], boxpoints=showScatter(data.size), row=1, col=position)
        position += 1    

    return fig