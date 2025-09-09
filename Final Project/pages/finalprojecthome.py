import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div([
    # Hero Section with Background Image
    html.Div([
        html.Div([
            html.H1("Let's take a trip to Colonial Williamsburg!", 
                   className="hero-title"),
            html.P("Step back in time and experience the charm of 18th-century America. Explore historic attractions, savor colonial cuisine, and plan your perfect visit with current weather conditions.", 
                   className="hero-subtitle"),
            html.Div([
                dcc.Link("Explore Attractions", href="/attractions", className="cta-button"),
                dcc.Link("Find Restaurants", href="/restaurants", className="cta-button secondary"),
                dcc.Link("Check Weather", href="/weather", className="cta-button"),
            ], className="cta-buttons")
        ], className="hero-content")
    ], className="hero-section")
], style={"margin": 0, "padding": 0})

