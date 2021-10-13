# -*- coding: utf-8 -*-

from dash.dependencies import Input, Output, State
from dash import dcc, html
from . import app

import pandas as pd

from . import ga
from .common import HIDE, SHOW, generate_table, upload_hint, parse_data

layout = html.Div(
    [
        upload_hint,
        dcc.Upload(id='ga_upload',
                   children=html.Div(
                       ['Drag and Drop or ',
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
        html.Div(id='ga_parsed_info'),
        html.Div(id='ga_parsed_data', style=HIDE),
        html.Div(id='ga_parsed_data_table'),
        html.Div(
            [
                html.Button(
                    'compute', id='ga_btn_compute', className="action-button"),
                html.Span([
                    "Mutation range",
                    dcc.Slider(
                        id="ga_mutation_slider",
                        min=-1,
                        max=1,
                        value=0,
                        step=0.01,
                        className="slider",
                        marks={
                            -1: "small",
                            1: "large",
                        },
                    ),
                    # remove style in order to show label
                    html.Span('', id="ga_mutation_slider_label", style=HIDE)
                ]),
                html.Div('', id='ga_compute_info')
            ],
            id='div_compute'),
    ],
    id="container",
    # tag for iframe resizer
    **{'data-iframe-height': ''},
)


@app.callback(Output('ga_mutation_slider_label', 'children'),
              [Input('ga_mutation_slider', 'value')])
def slider_output(value):
    """Callback for updating slider value"""
    return "{:5.2f}".format(10**value)


@app.callback([
    Output('ga_parsed_data', 'children'),
    Output('ga_parsed_info', 'children')
], [
    Input('ga_upload', 'contents'),
    Input('ga_upload', 'filename'),
    Input('ga_upload', 'last_modified')
])
def parse_data_ga(content, name, date):
    return parse_data(content, name, date)


@app.callback(Output('div_compute', 'style'),
              [Input('ga_parsed_data', 'children')])
def show_button(json):
    if json is None:
        return HIDE
    return SHOW


#@app.callback(Output('ga_parsed_data_table', 'children'), [Input('ga_parsed_data', 'children')])
#def show_data(json):
#    if json is None:
#        return ''
#    df = pd.read_json(json, orient='split')
#    return generate_table(df, download_link=False)
#
@app.callback(
    Output('ga_compute_info', 'children'),
    [Input('ga_btn_compute', 'n_clicks')],
    [
        State('ga_parsed_data', 'children'),
        State('ga_mutation_slider', 'value')
    ],
)
# pylint: disable=unused-argument, unused-variable
def on_compute(n_clicks, json, mutation_slider):
    if json is None:
        return ""
    df = pd.read_json(json, orient='split')

    new_pop, variables = ga.main(input_data=df.values,
                                 var_names=list(df),
                                 mutation_shrink_factor=10**mutation_slider)
    df_new = pd.DataFrame(new_pop, columns=variables)
    df_new['Fitness'] = ""

    return generate_table(df_new, download_link=True)
