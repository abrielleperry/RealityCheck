import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

file_path = '../data/fire.csv'
data = pd.read_csv(file_path)

data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour

pivot_table = data.pivot_table(
    index='time',
    columns='incident',
    aggfunc='size',
    fill_value=0)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Incident Analysis with Time Filter"),
    dcc.RangeSlider(
        id='time-range-slider',
        min=0,
        max=23,
        step=1,
        marks={i: f'{i:02d}:00' for i in range(24)},
        value=[0, 23]
    ),
    dcc.Graph(id='heatmap-graph')
])


@app.callback(
    Output('heatmap-graph', 'figure'),
    Input('time-range-slider', 'value')
)
def update_heatmap(time_range):
    filtered_data = data[(data['time'] >= time_range[0])
                         & (data['time'] <= time_range[1])]
    filtered_pivot = filtered_data.pivot_table(
        index='time', columns='incident', aggfunc='size', fill_value=0)
    fig = px.imshow(
        filtered_pivot,
        labels=dict(
            x="Incident Type",
            y="Hour of Day",
            color="Number of Incidents"),
        x=filtered_pivot.columns,
        y=filtered_pivot.index,
        aspect="auto")
    fig.update_layout(
        title="Correlation between Time of Day and Incident Types",
        xaxis_nticks=36)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
