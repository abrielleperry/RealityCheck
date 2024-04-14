import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('data/fire.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Property Distribution"),
    dcc.Graph(id='property-pie-chart')
])

# Define callback to update the pie chart


@app.callback(
    dash.dependencies.Output('property-pie-chart', 'figure'),
    [dash.dependencies.Input('dropdown-property', 'value')]
)
def update_pie_chart(selected_property):
    # Filter the dataframe based on the selected property
    filtered_df = df[df['property'] == selected_property]

    # Generate pie chart using Plotly Express
    fig = px.pie(
        filtered_df,
        names='property',
        title=f'Distribution of {selected_property}')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
