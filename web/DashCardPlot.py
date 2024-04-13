from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px

# Assuming 'order_details_df' is already fetched somewhere in your code
order_details_df = dp.fetch_order_details()
sales_order_df = dp.fetch_sales_order()


# Calculate daily revenue
daily_revenue = dp.compute_daily_revenue(order_details_df)

# Create a line chart
fig = px.line(daily_revenue, labels={'value': 'Gross Revenue', 'index': 'Order Date'},
              title='Daily Gross Revenue')
fig.update_layout(xaxis_title='Order Date', yaxis_title='Gross Revenue ($)')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up the app layout
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4("Gross Revenue Over Time", className="card-title"),
                        dcc.Graph(figure=fig)
                    ]
                ),
            ],
            className="mt-5",
        ),
    ],
    fluid=True,
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
