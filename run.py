# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
from dash.dependencies import Input, Output

from app import app
import ga
import maxdiv

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
    html.H2('Synthesis condition finder'),
    html.Ul([
        html.Li(html.A('Initialize diverse set', href='/maxdiv')),
        html.Li(html.A('Compute next generation', href='/ga')),
        html.Li(html.A('Determine importance of variables', href='/ml')),
    ])
]


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/maxdiv':
        return maxdiv.layout
    elif pathname == '/ga':
        return ga.layout
    return home


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
    #app.run_server()
