import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('../data/fire.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Property Distribution"),
    dcc.Graph(id='property-area-chart')
])

# Define callback to update the area chart


@app.callback(
    dash.dependencies.Output('property-area-chart', 'figure'),
    [dash.dependencies.Input('property-area-chart', 'id')]
)
def update_area_chart(selected_property):
    # Group by property and count occurrences
    property_counts = df['property'].value_counts().reset_index()
    property_counts.columns = ['property', 'count']

    # Generate area chart using Plotly Express
    fig = px.area(
        property_counts,
        x='property',
        y='count',
        title='Property Distribution')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
