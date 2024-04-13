# Import necessary libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load the CSV data into a DataFrame
df = pd.read_csv('data/tulsa-fire.csv')

# Check the DataFrame structure and modify as needed
print(df.head())  # This line is for debugging; you may remove it once everything is confirmed to work

# Initialize the Dash application
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Incidents Bar Chart"),
    dcc.Graph(id='bar-chart'),
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='incident'  # Replace with your column of interest
    )
])

# Callback to update the bar chart based on the selected column
@app.callback(
    Output('bar-chart', 'figure'),
    Input('column-selector', 'value')
)
def update_chart(incident):
    fig = px.bar(df, x=df.index, y=incident, title=f'Bar Chart of {incident}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
