# -*- coding: utf-8 -*-
"""Run app behind proxy server"""
import sys
import os
sys.path.insert(0, '/home/app')

from sycofinder import app, app_home, app_maxdiv, app_ga, app_ml
import dash.dependencies as dep


@app.callback(
    dep.Output('page-content', 'children'), [dep.Input('url', 'pathname')])
def display_page(pathname):
    if pathname is None:
        return app_home.layout

    if pathname.endswith('/maxdiv/'):
        return app_maxdiv.layout
    elif pathname.endswith('/ga/'):
        return app_ga.layout
    elif pathname.endswith('/ml/'):
        return app_ml.layout
    return app_home.layout

# See https://community.plot.ly/t/deploy-dash-on-apache-server-solved/4855/18
app_prefix = app.config['routes_pathname_prefix']
proxy_prefix = os.getenv('PROXY_PREFIX', app_prefix)

app.config.update({
    # Prefix for routes that flask should respond to.
    # Since proxy server redirects to localhost:1234/sycofinder/, this can
    # remain unmodified (could even be commented out)
    'routes_pathname_prefix': app_prefix,

    # Front-end will prefix this string to requests made to the proxy server.
    # This needs to be the prefix used by the proxy server
    'requests_pathname_prefix': proxy_prefix,
})

# app.server contains the Flask app
# See https://dash.plot.ly/deployment
application = app.server
