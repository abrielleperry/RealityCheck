# pip install dash pandas plotly
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your dataset
df = pd.read_csv('data/fire.csv')

# Ensure the 'date' column is treated as datetime type
df['date'] = pd.to_datetime(df['date'])

# Extract year and month for grouping
df['year_month'] = df['date'].dt.to_period('M')

# Create a Dash application
app = Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    dcc.Graph(id='incident-graph'),
    dcc.Dropdown(
        id='incident-type-dropdown',
        options=[{'label': i, 'value': i} for i in df['incident'].unique()],
        value=df['incident'].unique()[0]
    )
])

# Callback to update the graph based on selected incident type


@app.callback(
    Output('incident-graph', 'figure'),
    Input('incident-type-dropdown', 'value'))
def update_figure(selected_incident):
    # Filter data by selected incident type
    filtered_df = df[df.incident == selected_incident]

    # Group by year and month
    grouped_df = filtered_df.groupby(
        'year_month').size().reset_index(name='counts')

    # Plotting
    fig = px.line(grouped_df, x='year_month', y='counts',
                  title=f'Incident Type: {selected_incident} Over Time')

    # Update layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Incidents',
        xaxis_type='category')
    return fig


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
