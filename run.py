# -*- coding: utf-8 -*-
from sycofinder import app, app_home, app_maxdiv, app_ga, app_ml
import dash.dependencies as dep


@app.callback(
    dep.Output('page-content', 'children'), [dep.Input('url', 'pathname')])
def display_page(pathname):
    # pylint: disable=no-else-return
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
    app.run_server(debug=True, host='0.0.0.0')
