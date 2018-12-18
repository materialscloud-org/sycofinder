# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
from dash.dependencies import Input, Output

from sycofinder import app, app_maxdiv, app_ga, app_ml

# See https://community.plot.ly/t/deploy-dash-on-apache-server-solved/4855/18
app.config.update({
    # as the proxy server will remove the prefix
    'routes_pathname_prefix': '/',

    # the front-end will prefix this string to the requests
    # that are made to the proxy server
    'requests_pathname_prefix': '/sycofinder/'
})

title = 'Synthesis Condition Finder'

app.title = title
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Link(rel='stylesheet', href='/static/style.css'),
    html.Link(rel='stylesheet', href='/static/upload.css'),
    html.Div(id='page-content'),
    ## work around plot.ly dash design flaw
    ## https://community.plot.ly/t/display-tables-in-dash/4707/40
    #html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])

home = [
    html.H2(title),
    html.Ul([
        html.Li(html.A('Compute diverse set', href='/maxdiv')),
        html.Li(
            html.A('Genetic Algorithm: compute next generation', href='/ga')),
        html.Li(html.A('Determine importance of variables', href='/ml')),
    ])
]


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maxdiv':
        return app_maxdiv.layout
    elif pathname == '/ga':
        return app_ga.layout
    elif pathname == '/ml':
        return app_ml.layout
    return home


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
    #app.run_server()
