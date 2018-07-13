# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from cfinder import app

import plotly.graph_objs as go
import pandas as pd

from . import ml
from .common import HIDE, SHOW

graph_layout = dict(autosize=False, width=600, height=600)

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',
                           html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False),
    html.Div(id='ml_parsed_data', style=HIDE),
    html.Div(id='ml_parsed_data_table'),
    html.Div(
        [
            html.Button('compute', id='btn_compute'),
            dcc.Graph(
                id='bar-chart', figure=dict(layout=graph_layout, data=[])),
            html.Div('', id='ga_compute_info')
        ],
        id='ml_div_compute',
        style=HIDE)
])


@app.callback(
    Output('ml_parsed_data', 'children'), [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
        Input('upload-data', 'last_modified')
    ])
def update_output(content, name, date):
    if content is None:
        return ''

    from .common import validate_df, parse_contents

    df = parse_contents(content, name, date)
    validate_df(df)
    return df.to_json(date_format='iso', orient='split')


@app.callback(
    Output('ml_div_compute', 'style'), [Input('ml_parsed_data', 'children')])
def show_button(json):
    if json is None:
        return HIDE
    return SHOW

# pylint: disable=unused-argument
@app.callback(
    Output('bar-chart', 'figure'), [Input('btn_compute', 'n_clicks')],
    [State('ml_parsed_data', 'children')])
def on_compute(n_clicks, json):
    df = pd.read_json(json, orient='split')
    var_imp = ml.main(input_data=df.values, var_names=list(df))

    #marker = dict(size=10, line=dict(width=2), color=clrs, colorscale=colorscale, colorbar=colorbar)
    trace = go.Bar(
        x=list(df)[:-1],
        y=var_imp,
    )

    graph_layout.update(
        dict(
            title="Importance of variables",
            xaxis=dict(title="Variable"),
            yaxis=dict(title="Importance"),
            hovermode='closest'))

    figure = dict(data=[trace], layout=graph_layout)
    return figure

    #df_new = pd.DataFrame(new_pop, columns=variables)

    #from common import generate_table
    #return generate_table(df_new, download_link=True)
