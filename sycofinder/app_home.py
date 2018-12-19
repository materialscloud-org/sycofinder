import dash_html_components as html
from . import app

layout = [
    html.H2(app.title),
    html.Div(
        [
            html.H2("About"),
            html.Div("It's me"),
            html.H2("Acknowledgements"),
            html.Div("It's me"),
        ],
        id="accordion",
    ),
    html.Ul([
        html.Li(html.A('Compute diverse set', href='maxdiv/')),
        html.Li(
            html.A('Genetic Algorithm: compute next generation', href='ga/')),
        html.Li(html.A('Determine importance of variables', href='ml/')),
    ])
]
