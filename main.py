import dash
from dash import html

app = dash.Dash(__name__, use_pages=True, pages_folder="src/pages")

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    print("Lancement sur http://127.0.0.1:8053/")
    app.run(debug=True, port=8053)