# components.py

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

def create_small_card(gross_revenue, fig):
    small_card = dbc.Card(
        [
            dbc.CardBody(
                [                   
                    html.H4("Gross Revenue", className="card-title"),
                    html.H5(f"${gross_revenue:,.2f}", className="card-text"),
                    dcc.Graph(figure=fig)
                ]
            ),
        ],
        style={"width": "100%"}
    )
    return small_card
