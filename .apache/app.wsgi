# -*- coding: utf-8 -*-
"""Run app behind proxy server"""
import sys
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


## See https://community.plot.ly/t/deploy-dash-on-apache-server-solved/4855/18
#app.config.update({
#    # as the proxy server will remove the prefix
#    'routes_pathname_prefix': '/',
#
#    # the front-end will prefix this string to the requests
#    # that are made to the proxy server
#    'requests_pathname_prefix': '/sycofinder/'
#})

# app.server containes the Flask app
# See https://dash.plot.ly/deployment
application = app.server

#app.run_server(host='0.0.0.0')
