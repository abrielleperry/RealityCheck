# Importing necessary libraries
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Load the CSV data
df = pd.read_csv("Tulsa-Fire.csv")  # Make sure to replace 'your_data.csv' with your actual file path

# Assume 'date' is the column with dates, and 'incident' is the column recording each incident
# Parsing the 'date' column into datetime
df['date'] = pd.to_datetime(df['date'])

# Extracting month from the date
df['month'] = df['date'].dt.to_period('M')

# Aggregating data to count incidents per month
monthly_incidents = df.groupby('month').size().reset_index(name='counts')

# Creating the Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Incidents per Month"),
        dcc.Graph(
            id='incident-bar-chart',
            figure=px.bar(
                monthly_incidents,
                x='month',
                y='counts',
                title="Monthly Incidents",
                labels={"month": "Month", "counts": "Number of Incidents"},
                template="plotly_dark"
            )
        )
    ])
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
