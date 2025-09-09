from dash import html, register_page, dcc, callback, Output, Input
import requests
from bs4 import BeautifulSoup
import random
import dash_bootstrap_components as dbc

register_page(__name__, path="/attractions", name="Attractions")

layout = dbc.Container([
    # Hero Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Discover Williamsburg", className="attractions-hero-title"),
                html.P("Explore the best attractions and experiences in Williamsburg", className="attractions-hero-subtitle"),
                dbc.Button([
                    html.I(className="fas fa-dice me-2"),
                    "Find My Adventure"
                ], id="btn-attraction", n_clicks=0, className="attractions-discover-btn")
            ], className="attractions-hero-content")
        ], width=12)
    ], className="attractions-hero-section"),
    
    # Main Content
    dbc.Row([
        dbc.Col([
            dcc.Loading(
                html.Div(id="attraction-site", className="attraction-result-container"),
                type="circle",
                color="#8B4513"
            )
        ], width=12)
    ], className="attractions-main-content")
], fluid=True, className="attractions-container")

# Fallback list
FALLBACK_ATTRACTIONS = [
    {"name": "Colonial Williamsburg (Governor's Palace, trades, reenactments)", "rating": 89},
    {"name": "DeWitt Wallace Decorative Arts Museum", "rating": 80},
    {"name": "Abby Aldrich Rockefeller Folk Art Museum", "rating": 90},
    {"name": "Muscarelle Museum of Art", "rating": 90},
    {"name": "Busch Gardens Williamsburg", "rating": 94},
    {"name": "Water Country USA", "rating": 94},
    {"name": "Jamestown Settlement", "rating": 91},
    {"name": "American Revolution Museum at Yorktown", "rating": 50},
    {"name": "Kimball Theatre", "rating": 92},
    {"name": "Merchants Square", "rating": 88}
]


ATTRACTIONS_IMAGES = {
    "Colonial Williamsburg (Governor's Palace, trades, reenactments)": "colonials williamsburg.jpg",
    "DeWitt Wallace Decorative Arts Museum": "dewitt.jpg",
    "Abby Aldrich Rockefeller Folk Art Museum": "folkart.jpg",
    "Muscarelle Museum of Art": "muscarelle.jpg",
    "Busch Gardens Williamsburg": "buschgardens.jpg",
    "Water Country USA": "water country.jpg",
    "Jamestown Settlement": "jamestown settelment.jpg",
    "American Revolution Museum at Yorktown": "american revolution (1).jpg",
    "Kimball Theatre": "kimball.jpg",
    "Merchants Square": "merchants square.jpg"
}


def fetch_attractions():
    try:
        url = "https://www.visitwilliamsburg.com/things-to-do/museums-and-attractions/"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml')
        blocks = soup.select('div.attraction-item')
        attractions = [
            blk.get_text(strip=True)
            for blk in blocks
            if blk.get_text(strip=True)
        ]
        return attractions if attractions else FALLBACK_ATTRACTIONS
    except Exception:
        return FALLBACK_ATTRACTIONS


# ✅ COMBINED callback for name and image
@callback(
    Output("attraction-site", "children"),
    Input("btn-attraction", "n_clicks")
)
def update_attraction(n_clicks):
    if not n_clicks:
        return html.Div([
            html.Div([
                html.I(className="fas fa-map-marker-alt attractions-placeholder-icon"),
                html.H3("Ready to Explore?", className="attractions-placeholder-title"),
                html.P("Click the button above to discover your next adventure in Williamsburg!", className="attractions-placeholder-text")
            ], className="attractions-placeholder")
        ], className="attraction-result-container")

    attractions = fetch_attractions()
    selected = random.choice(attractions)
    
    # Handle both dict and string formats
    if isinstance(selected, dict):
        attraction_name = selected["name"]
        attraction_rating = selected.get("rating", 0)
    else:
        attraction_name = selected
        attraction_rating = 0

    # Get image file
    image_file = ATTRACTIONS_IMAGES.get(attraction_name, "other.jpg")
    image_path = f"/assets/{image_file}"
    
    # Create star rating
    stars = "★" * (attraction_rating // 20) + "☆" * (5 - (attraction_rating // 20))
    
    # Create image section - show fallback if no image file
    if image_file == "other.jpg" or not image_file:
        image_section = html.Div([
            html.I(className="fas fa-image attraction-fallback-icon"),
            html.Span("Image not available", className="attraction-fallback-text")
        ], className="attraction-image-fallback")
    else:
        image_section = html.Img(src=image_path, className="attraction-image")
    
    # Create modern attraction card
    attraction_card = html.Div([
        html.Div([
            html.Div([
                image_section
            ], className="attraction-image-container"),
            html.Div([
                html.Div([
                    html.H2(attraction_name, className="attraction-name"),
                    html.Div([
                        html.Span(stars, className="attraction-rating"),
                        html.Span(f"{attraction_rating}/100", className="attraction-rating-number")
                    ], className="attraction-rating-container")
                ], className="attraction-header"),
                html.Div([
                    html.I(className="fas fa-map-marker-alt attraction-icon"),
                    html.Span("Williamsburg, VA", className="attraction-location")
                ], className="attraction-location-container"),
                html.Div([
                    html.I(className="fas fa-star attraction-icon"),
                    html.Span("Highly Recommended", className="attraction-recommendation")
                ], className="attraction-recommendation-container")
            ], className="attraction-content")
        ], className="attraction-card")
    ], className="attraction-result")

    return attraction_card

