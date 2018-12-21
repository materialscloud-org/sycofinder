# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

#app = dash.Dash(__name__)
app = dash.Dash(__name__, url_base_pathname='/sycofinder/')
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
