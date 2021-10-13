# -*- coding: utf-8 -*-
import dash
from dash import html, dcc

#app_prefix = '/sycofinder'
app_prefix = ''

#app = dash.Dash(__name__)
app = dash.Dash(
    __name__,
    url_base_pathname=app_prefix + '/',
    assets_url_path=app_prefix + '/assets',
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
        # needed for iframe resizer
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        },
    ])
server = app.server
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

title = 'Synthesis Condition Finder'

app.title = title
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    #html.Link(rel='stylesheet', href='/static/style.css'),
    #html.Link(rel='stylesheet', href='/static/upload.css'),
    html.Div(id='page-content'),
    ## work around plot.ly dash design flaw
    ## https://community.plot.ly/t/display-tables-in-dash/4707/40
    #html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])
