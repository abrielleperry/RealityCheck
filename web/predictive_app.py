import dash
from dash import dcc, html  # Updated import statements
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pickle

# Load your trained model (assuming it's saved as 'model.pkl')
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[
                'https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.H1("Emergency Incident Prediction Dashboard"),
    html.Div([
        html.Div([
            dcc.DatePickerSingle(
                id='input-date',
                min_date_allowed=pd.to_datetime('2021-01-01'),
                max_date_allowed=pd.to_datetime('2023-12-31'),
                initial_visible_month=pd.to_datetime('2023-01-01'),
                date=str(pd.to_datetime('2023-01-01'))
            ),
        ], style={'margin': '20px'}),
        html.Button('Predict', id='predict-button', n_clicks=0),
        html.Div(id='prediction-output', style={'margin': '20px'})
    ]),
    dcc.Graph(id='feature-importance-plot')
])


@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [dash.dependencies.State('input-date', 'date')]
)
def update_output(n_clicks, date):
    if n_clicks > 0:
        # Example feature preparation based on date input (needs proper
        # implementation)
        features = np.random.rand(1, 10)  # Example features
        prediction = model.predict(features)[0]
        return f"Predicted number of incidents on {date}: {prediction:.0f}"


@app.callback(
    Output('feature-importance-plot', 'figure'),
    [Input('predict-button', 'n_clicks')]
)
def update_graph(n_clicks):
    if n_clicks > 0:
        importances = model.feature_importances_
        features = ['feature_' + str(i) for i in range(len(importances))]
        df = pd.DataFrame({
            'Feature': features,
            'Importance': importances
        })
        fig = px.bar(
            df,
            x='Feature',
            y='Importance',
            title='Feature Importances')
        return fig
    return dash.no_update


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
