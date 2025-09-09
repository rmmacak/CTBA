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
    except requests.RequestException as e:
        return pd.DataFrame(columns=["time", "temp_F"])  # stores as list with time and temperature

# Layout
layout = dbc.Container([
    # Hero Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Weather Forecast", className="weather-hero-title"),
                html.P("Williamsburg, VA", className="weather-hero-subtitle"),
                dbc.Button([
                    html.I(className="fas fa-sync-alt me-2"),
                    "Refresh Weather"
                ], id="refresh-btn", n_clicks=0, className="weather-refresh-btn")
            ], className="weather-hero-content")
        ], width=12)
    ], className="weather-hero-section"),
    
    # Main Content
    dbc.Row([
        # Left Column - Weather Cards
        dbc.Col([
            html.Div([
                # Current Temperature Card
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-thermometer-half", style={"font-size": "1.5rem"})
                        ], className="weather-icon-circle current-temp-icon"),
                        html.Div([
                            html.H3("Current Temperature", className="weather-card-title"),
                            html.Div(id="kpi-now", className="weather-current-temp")
                        ], className="weather-card-content")
                    ], className="weather-card-header"),
                    html.Div([
                        html.Span("°F", className="weather-temp-unit")
                    ], className="weather-card-footer")
                ], className="weather-card current-temp-card"),
                
                # Temperature Range Card
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-temperature-low", style={"font-size": "1.5rem"})
                        ], className="weather-icon-circle range-icon"),
                        html.Div([
                            html.H3("Temperature Range", className="weather-card-title"),
                            html.Div([
                                html.Div([
                                    html.Span("Min", className="weather-range-label"),
                                    html.Span(id="kpi-min", className="weather-range-value")
                                ], className="weather-range-item"),
                                html.Div([
                                    html.Span("Max", className="weather-range-label"),
                                    html.Span(id="kpi-max", className="weather-range-value")
                                ], className="weather-range-item")
                            ], className="weather-range-container")
                        ], className="weather-card-content")
                    ], className="weather-card-header")
                ], className="weather-card range-card"),
                
                # Summary Stats Card
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-bar", style={"font-size": "1.5rem"})
                        ], className="weather-icon-circle stats-icon"),
                        html.Div([
                            html.H3("Summary Stats", className="weather-card-title"),
                            dcc.Loading(html.Div(id="stats-table", className="weather-stats-table"))
                        ], className="weather-card-content")
                    ], className="weather-card-header")
                ], className="weather-card stats-card")
            ], className="weather-cards-container")
        ], md=5),
        
        # Right Column - Chart
        dbc.Col([
            html.Div([
                html.Div([
                    html.I(className="fas fa-chart-line weather-chart-icon"),
                    html.H3("Hourly Temperature Forecast", className="weather-chart-title")
                ], className="weather-chart-header"),
                dcc.Loading(
                    dcc.Graph(id="temp-chart", config={"displayModeBar": False}),
                    type="circle",
                    color="#8B4513"
                )
            ], className="weather-chart-container")
        ], md=7)
    ], className="weather-main-content")
], fluid=True, className="weather-container")

# Callback
@callback(
    [
        Output("temp-chart", "figure"), # graph
        Output("kpi-now", "children"), # weather now
        Output("kpi-min", "children"), # low
        Output("kpi-max", "children"), # high
        Output("stats-table", "children"), 
    ],
    [Input("refresh-btn", "n_clicks")],
    prevent_initial_call=False
)
def update_weather(n_clicks):
    df = fetch_hourly_temp(LAT, LON) # function that gets weather
    
    if df.empty:
        empty_fig = px.line()
        empty_fig.update_layout(
            title="No weather data available",
            xaxis_title="Time",
            yaxis_title="Temperature (°F)"
        )
        return empty_fig, "N/A", "N/A", "N/A", html.Div("No weather data available", className="weather-no-data")
    
    now = df.iloc[0]["temp_F"] # temp now
    tmin = df["temp_F"].min() # low
    tmax = df["temp_F"].max() # high
    
    fig = px.line(df, x="time", y="temp_F", markers=True) # graph layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", size=12),
        yaxis=dict(
            title=dict(text="Temperature (°F)", font=dict(size=14, color="#495057")),
            tickfont=dict(size=12, color="#6c757d"),
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False
        ),
        xaxis=dict(
            title=dict(text="Time", font=dict(size=14, color="#495057")),
            tickfont=dict(size=12, color="#6c757d"),
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        )
    )
    
    # Update line styling
    fig.update_traces(
        line=dict(color='#8B4513', width=3),
        marker=dict(color='#A0522D', size=6, line=dict(color='white', width=2)),
        hovertemplate='<b>%{x}</b><br>Temperature: %{y:.1f}°F<extra></extra>'
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
        html.Thead([
            html.Tr([
                html.Th(c, className="weather-table-header") for c in summary.columns
            ])
        ], className="weather-table-head"),
        html.Tbody([
            html.Tr([
                html.Td(v, className="weather-table-cell") for v in row
            ], className="weather-table-row") for row in summary.values
        ], className="weather-table-body")
    ], className="weather-table")
    
    fmt = lambda x: f"{x:.1f}"
    return fig, fmt(now), fmt(tmin), fmt(tmax), table  # returns all necessary values
