import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load the CSV data
data = pd.read_csv('../data/fire.csv')

# Filter data where location_name is 'hse'
filtered_data = data[data['location_name'].str.lower() == 'hse']

# Count the frequency of each incident
incident_counts = filtered_data['incident'].value_counts().reset_index()
incident_counts.columns = ['incident', 'count']

# Filter to include only incidents with count greater than a specific threshold
threshold = 10  # Set this to your desired threshold
filtered_incidents = incident_counts[incident_counts['count'] > threshold]

# Create a bar graph for the 'incident' column
fig = px.bar(filtered_incidents, x='incident', y='count', title='Frequency of Incidents at Location "HSE"', color='incident',  # This assigns a unique color based on the 'incident' column
             color_continuous_scale=px.colors.qualitative.Plotly)

# Set graph size
fig.update_layout(width=1200, height=800)

# Adjust y-axis to include all incidents plus some additional space
max_count = filtered_incidents['count'].max()
fig.update_yaxes(range=[0, max_count + 82])

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Incident Analysis for Houses'),
    dcc.Graph(
        id='incident-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
