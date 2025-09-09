import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc


#initialize the app
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, title = "Colonial Williamsburg Travel Guide", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server #for deployment

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="/assets/style.css">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)
