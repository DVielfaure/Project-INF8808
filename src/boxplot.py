import plotly.graph_objects as go
from plotly.subplots import make_subplots

MAX_DISPLAYED_POINTS = 99999

def boxplot(dataY, name, color):
    points = False if dataY.size > MAX_DISPLAYED_POINTS else 'all'

    return go.Box(
        y=dataY,
        name=name,
        boxpoints=points,
        jitter=0.4,
        whiskerwidth=0.2,
        fillcolor=color,
        marker_size=6,
        marker_opacity=0.5,
        line_width=1,
        boxmean=True,
    )


def trace_boxplot(df):

    fig = make_subplots(rows=1, cols=4)

    fig.add_trace(boxplot(df['Lenght'], 'Longueur (m)', 'rgba(93, 164, 214, 0.5)'), row=1, col=1)
    fig.add_trace(boxplot(df['Width'], 'Largeur (m)', 'rgba(255, 144, 14, 0.5)'), row=1, col=2)
    fig.add_trace(boxplot(df['DeadWeight Tonnage'], 'Capacité Maximale (kg)', 'rgba(44, 160, 101, 0.5)'), row=1, col=3)
    fig.add_trace(boxplot(df['Maximum Draugth'], "Tirant d'eau maximal (m)", 'rgba(255, 65, 54, 0.5)'), row=1, col=4)

    fig.update_layout(
        title='Distribution des dimensions des navires',
        height=800,
        showlegend=False,
    )

    return fig


def update_traces_boxplot(df, fig, region, harbour):
    if (harbour != None):
        data = df[df['Departure Hardour'] == harbour]
    elif (region != None):
        data = df[df['Departure Region'] == region]
    else: 
        data = df

    points = False if data.size > MAX_DISPLAYED_POINTS else 'all'
    fig.update_traces(y=data['Lenght'], boxpoints=points, row=1, col=1)
    fig.update_traces(y=data['Width'], boxpoints=points, row=1, col=2)
    fig.update_traces(y=data['DeadWeight Tonnage'], boxpoints=points, row=1, col=3)
    fig.update_traces(y=data['Maximum Draugth'], boxpoints=points, row=1, col=4)    

    fig.update_layout(title=f"Size: {data.size} | Distribution des dimensions des navires dans la region de {region}, le port {harbour}")
    return fig