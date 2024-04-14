from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('data/fire.csv')

# Ensure the 'incident' column is of string type and drop any rows where
# 'incident' is null
df = df.dropna(subset=['incident'])
df['incident'] = df['incident'].astype(str)

# Convert 'date' to datetime and extract the month as 'YYYY-MM' format for
# simplicity
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%Y-%m')

# Group by month and incident type
monthly_incidents = df.groupby(
    ['month', 'incident']).size().reset_index(name='count')

# Create the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Incident Reports Over Time"),
    dcc.Dropdown(
        id='incident-dropdown',
        options=[{'label': i, 'value': i}
                 for i in df['incident'].unique() if i is not None],
        # Default value, assuming there is at least one incident type
        value=df['incident'].unique()[0]
    ),
    dcc.Graph(id='incident-graph')
])


@app.callback(
    Output('incident-graph', 'figure'),
    Input('incident-dropdown', 'value'))
def update_graph(selected_incident):
    filtered_data = monthly_incidents[monthly_incidents['incident']
                                      == selected_incident]

    fig = px.line(filtered_data, x='month', y='count',
                  title=f'Monthly Count of {selected_incident}')
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Number of Incidents')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
