import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H2("Let's take a trip to Colonial Williamsburg!"),
    html.P("Please click any option that you would like to explore!")
    
])