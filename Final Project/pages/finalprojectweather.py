# import necessary packages to plot the weather 
from dash import html, dcc, callback, Input, Output, register_page
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import dash_bootstrap_components as dbc

# Register Page
register_page(__name__, path='/weather', name="Weather")

# Williamsburg coordinates
LAT, LON = 37.2707, -76.7075

# Get hourly temperature
def fetch_hourly_temp(lat, lon):
    # api that we use to get the weather 
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m&forecast_days=2&timezone=auto"
    )
    try:
        r = requests.get(url, timeout=15)  # timeout after 15 seconds
        r.raise_for_status()
        data = r.json()["hourly"]  # stores temperatures 
        df = pd.DataFrame({"time": data["time"], "temp_C": data["temperature_2m"]}) 
        df["time"] = pd.to_datetime(df["time"])
        # Convert Celsius to Fahrenheit
        df["temp_F"] = df["temp_C"] * 9/5 + 32
        return df
    except requests.RequestException:
        return pd.DataFrame(columns=["time", "temp_F"])  # stores as list with time and temperature

# Layout
layout = dbc.Container([
    html.H1("Weather Forecast - Williamsburg"),  # title
    
    dbc.Button("Refresh", id="refresh-btn", n_clicks=0, color="primary"),  # refresh button
    html.Br(), html.Br(),
    
    dbc.Row([
        dbc.Col([
            html.H4("Current Temperature (°F)"), # heading
            html.Div(id="kpi-now", style={"fontSize": "2rem", "margin-bottom": "20px"}), # temperature right now
            html.H4("Temperature Range (°F)"), # highs and lows for the day
            html.Div([
                html.Span("Min: "), html.Span(id="kpi-min", style={"margin-right": "20px"}), # low
                html.Span("Max: "), html.Span(id="kpi-max") # high
            ], style={"fontSize": "1.2rem", "margin-bottom": "20px"}),
            html.H4("Summary Stats"), # weather for today and tomorrow
            dcc.Loading(html.Div(id="stats-table"))
        ], md=5),
        
        dbc.Col([
            html.H4("Hourly Temperature (Next 48h)"), # graph of temperature over the next 48 hours
            dcc.Loading(dcc.Graph(id="temp-chart", config={"displayModeBar": False}))
        ], md=7)
    ])
], fluid=True)

# Callback
@callback(
    [
        Output("temp-chart", "figure"), # graph
        Output("kpi-now", "children"), # weather now
        Output("kpi-min", "children"), # low
        Output("kpi-max", "children"), # high
        Output("stats-table", "children"), 
    ],
    [Input("refresh-btn", "n_clicks")]
)
def update_weather(_):
    df = fetch_hourly_temp(LAT, LON) # function that gets weather
    
    if df.empty:
        empty_fig = px.line()
        return empty_fig, "N/A", "N/A", "N/A", "No data available" # if weather does not work
    
    now = df.iloc[0]["temp_F"] # temp now
    tmin = df["temp_F"].min() # low
    tmax = df["temp_F"].max() # high
    
    fig = px.line(df, x="time", y="temp_F", markers=True) # graph layout
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), 
        yaxis_title="°F", 
        xaxis_title="Time"
    )
    
    summary = (
        df.assign(Date=df["time"].dt.date)
        .groupby("Date")["temp_F"]
        .agg(["min", "max", "mean"])
        .round(1)
        .rename(columns={"min": "Min °F", "max": "Max °F", "mean": "Avg °F"})
        .reset_index()
    )
    
    table = html.Table([
        html.Thead(html.Tr([html.Th(c) for c in summary.columns])),
        html.Tbody([html.Tr([html.Td(v) for v in row]) for row in summary.values])
    ])
    
    fmt = lambda x: f"{x:.1f}"
    return fig, fmt(now), fmt(tmin), fmt(tmax), table  # returns all necessary values