import dash_html_components as html
from . import app

layout = [
    html.Div(
        [
            html.Div(html.H1(app.title), id="maintitle"),
            html.H2("About"),
            html.P("""
We report a methodology using machine learning to capture chemical intuition
from a set of (partially) failed attempts to synthesize a metal organic
framework. We define chemical intuition as the collection of unwritten
guidelines used by synthetic chemists to find the right synthesis conditions.
As (partially) failed experiments usually remain unreported, we have
reconstructed a typical track of failed experiments in a successful search for
finding the optimal synthesis conditions that yields HKUST-1 with the highest
surface area reported to date. We illustrate the importance of quantifying this
chemical intuition for the synthesis of novel materials.
"""),
            html.Ul([
                html.Li(html.A('Compute diverse set', href='maxdiv/')),
                html.Li(
                    html.A(
                        'Genetic Algorithm: compute next generation',
                        href='ga/')),
                html.Li(
                    html.A('Determine importance of variables', href='ml/')),
            ]),
        ],
        id="container")
]
