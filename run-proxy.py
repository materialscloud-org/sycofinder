# -*- coding: utf-8 -*-
"""Run app behind proxy server"""

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


if __name__ == '__main__':
    # See https://community.plot.ly/t/deploy-dash-on-apache-server-solved/4855/18
    app.config.update({
        # as the proxy server will remove the prefix
        'routes_pathname_prefix': '/',

        # the front-end will prefix this string to the requests
        # that are made to the proxy server
        'requests_pathname_prefix': '/sycofinder/'
    })

    app.run_server(host='0.0.0.0')
