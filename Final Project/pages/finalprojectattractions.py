from dash import html, register_page, dcc, callback, Output, Input
import requests
from bs4 import BeautifulSoup
import random

register_page(__name__, path="/attractions", name="Attractions")

layout = html.Div([
    html.H2("Attractions", className="page-title"),
    html.P("Click the button and see where you go today!", className="page-subtitle"),
    html.Button("Attraction Button", id="btn-attraction", n_clicks=0),
    dcc.Loading(html.Div(id="attraction-site")),
    html.Img(id="attractions-img", style={
        "width": "100%",
        "max-width": "600px",
        "margin-bottom": "20px",
        "align-items": "center"
    }),
], className="attractions-wrap")

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
    Output("attractions-img", "src"),
    Input("btn-attraction", "n_clicks")
)
def update_attraction(n_clicks):
    if not n_clicks:
        return "", ""

    attractions = fetch_attractions()
    selected = random.choice(attractions)

    text = f"🎡 Your attraction: {selected}"
    image_file = ATTRACTIONS_IMAGES.get(selected)

    if image_file:
        image_path = f"/assets/{image_file}"
    else:
        image_path = ""

    return html.Div(text, className="attraction-result"), image_path

