import dash_html_components as html
from . import app

about = """
SyCoFinder was designed to aid experiments in order to efficiently explore the
chemical space involved in the synthesis of metal-organic frameworks.

The first component of the app generates a diverse set of synthesis conditions
in the chemical space defined by the user (potentially already including chemical
intuition by assigning variable importance).

Users then perform experiments, recording the fitness of the samples obtained
(fitness scores are user specific, higher is better).  These records are fed
into the second component of the app, which optimizes the synthesis conditions
using a genetic algorithm.

Finally, the complete set of experiments and fitness records can be used to determine
the importance of experimental variables using a machine learning algorithm.
"""

changelog = [
    ["v0.1.1", "reduce max number of variables to 5"],
    ["v0.1.0", "release on Materials Cloud"],
]

about_html = [html.P(i) for i in about.split("\n\n")]

layout = [
    html.Div(
        [
            html.Div(html.H1(app.title), id="maintitle"),
            html.H2("About"),
            html.Img(src="assets/images/logo.png", className="sycologo"),
            html.Img(src="assets/images/schema.png", className="sycoschema"),
            html.Div(
                about_html + [
                    html.P(
                        html.A(
                            html.B("Watch the tutorial on Youtube"),
                            href='https://youtu.be/i8i4HmEEw4Y',
                            target='_blank')),
                ],
                className="info-container"),
            html.H2("Steps"),
            html.Div(
                html.Ol([
                    html.Li(html.A('Compute diverse set', href='maxdiv/')),
                    html.Li(
                        html.A(
                            'Genetic Algorithm: compute next generation',
                            href='ga/')),
                    html.Li(
                        html.A(
                            'Determine importance of variables', href='ml/')),
                ]),
                className="sycolinks"),
            html.H2("Changelog"),
            html.Ul([
                html.Li([html.B(k + " "), html.Span(v)]) for k, v in changelog
            ]),
        ],
        id="container",
        # tag for iframe resizer
        **{'data-iframe-height': ''},
    )
]
