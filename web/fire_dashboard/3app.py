import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from dash.dependencies import Input, Output
from flask import Flask, render_template

# Initialize Flask and Dash
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Interactive Incident Report",
)


def initialize_data():
    static_df = pd.read_csv("../data/fire.csv")
    static_df.dropna(subset=["incident"], inplace=True)
    static_df["incident"] = static_df["incident"].astype(str)
    static_df["date"] = pd.to_datetime(static_df["date"])
    static_df["month"] = static_df["date"].dt.strftime("%Y-%m")
    monthly_incidents = (static_df.groupby(
        ["month", "incident"]).size().reset_index(name="count"))

    url = "https://www.cityoftulsa.org/apps/opendata/tfd_dispatch.jsn"
    live_df = pd.read_json(url)
    incidents = pd.json_normalize(live_df["Incidents"]["Incident"])
    incidents["Latitude"] = pd.to_numeric(
        incidents["Latitude"], errors="coerce")
    incidents["Longitude"] = pd.to_numeric(
        incidents["Longitude"], errors="coerce")
    incidents["ResponseDate"] = pd.to_datetime(
        incidents["ResponseDate"], format="%m/%d/%Y %I:%M:%S %p"
    )
    incidents["Year"] = incidents["ResponseDate"].dt.year
    incidents["Month"] = incidents["ResponseDate"].dt.month

    years = incidents["Year"].unique()
    months = incidents["Month"].unique()
    problems = incidents["Problem"].unique()

    return static_df, monthly_incidents, years, months, problems, incidents


static_df, monthly_incidents, years, months, problems, incidents = initialize_data()


# Define a Flask route
@server.route("/time_incident")
def time_incident():
    file_path = "../data/fire.csv"
    data = pd.read_csv(file_path)

    data["time"] = pd.to_datetime(data["time"], format="%H:%M:%S").dt.hour
    pivot_table = data.pivot_table(
        index="time", columns="incident", aggfunc="size", fill_value=0
    )

    fig = px.imshow(
        pivot_table,
        labels=dict(
            x="Incident Type",
            y="Hour of Day",
            color="Number of Incidents"),
        x=pivot_table.columns,
        y=pivot_table.index,
        aspect="auto",
        title="Correlation between Time of Day and Incident Types",
    )
    fig.update_layout(xaxis_nticks=36)

    return render_template("time_incident.html", graph=fig.to_html())


app.layout = dbc.Container([html.H1("Interactive Incident Report"),
                            dbc.Row([dbc.Col([html.Label("Select Incident Type:"),
                                              dcc.Dropdown(id="incident-type-dropdown",
                                    options=[{"label": i,
                                              "value": i} for i in static_df["incident"].dropna().unique()],
                                    value=static_df["incident"].dropna().unique()[0],
                                    multi=True,
                                    ),
                                dcc.Graph(id="action-taken-bar-chart"),
                            ],
                                md=4,
                            ),
                                dbc.Col([html.Label("Select Year:"),
                                         dcc.Dropdown(id="year-filter",
                                                      options=[{"label": year,
                                                                "value": year} for year in sorted(years)],
                                                      value=sorted(years)[0],
                                                      multi=False,
                                                      ),
                                         html.Label("Select Month:"),
                                         dcc.Dropdown(id="month-filter",
                                                      options=[{"label": month,
                                                                "value": month} for month in sorted(months)],
                                                      value=sorted(months)[0],
                                                      multi=False,
                                                      ),
                                         html.Label("Select Problems:"),
                                         dbc.Checklist(id="problem-filter",
                                                       options=[{"label": "Unselect All",
                                                                 "value": "None"},
                                                                {"label": "Select All",
                                                                 "value": "All"},
                                                                ] + [{"label": problem,
                                                                      "value": problem} for problem in problems],
                                                       value=["All"],
                                                       inline=False,
                                                       ),
                                         dcc.Graph(id="incident-map",
                                                   style={"width": "100%",
                                                          "height": "600px"},
                                                   ),
                                         ],
                                        md=8,
                                        ),
                            ]),
                            html.Div([html.H1("Live Incident Pie Chart"),
                                      dcc.Graph(id="live-incident-pie-chart"),
                                      ]),
                            html.Div([html.H1("Incident Reports Over Months"),
                                      dcc.Dropdown(id="incident-dropdown",
                                                   options=[{"label": i,
                                                             "value": i} for i in static_df["incident"].unique() if i is not None],
                                                   value=static_df["incident"].unique()[0],
                                                   ),
                                      dcc.Graph(id="incident-over-months-chart"),
                                      ]),
                            ])

# Define the callbacks and fetch_live_data function as previously described
# Callbacks and fetch_live_data function are not included here due to
# length constraints

if __name__ == "__main__":
    app.run_server(debug=True)
