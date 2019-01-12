# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
from builtins import range  # pylint: disable=redefined-builtin

import collections

import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt

import pandas as pd
import numpy as np
#from . import uniform
from . import maxmin
from . import app

# variables
variables = collections.OrderedDict([
    ('temperature', dict(
        label='Temperature [C]', range=[100.0, 200.0], weight=1.0)),
    ('r_ratio', dict(label='Reactants ratio', range=[0.8, 1.8], weight=1.0)),
    #    ('power',
    #     dict(label='Microwave Power [W]', range=[150.0, 250.0], weight=2.0)),
    ('h2o', dict(label='Water [ml]', range=[1.0, 6.0], weight=1.0)),
    #    ('dmf', dict(label='DMF [ml]', range=[1.0, 6.0], weight=1.0)),
    #    ('time', dict(label='Reaction time [min]', range=[2.0, 60.0], weight=2.0)),
    #    ('etoh', dict(label='Ethanol [ml]', range=[1.0, 6.0], weight=1.0)),
    #    ('meoh', dict(label='Methanol [ml]', range=[1.0, 6.0], weight=1.0)),
    #    ('iproh', dict(
    #        label='Isopropyl alcohol [ml]', range=[1.0, 6.0], weight=1.0)),
])
NVARS_DEFAULT = len(variables)

# Fill up to NVARS_MAX (needed to define callbacks)
# Note: In the current implementation, anything beyond 6 takes too much time
NVARS_MAX = 5
for i in range(len(variables), NVARS_MAX):
    k = 'variable_{}'.format(i + 1)
    variables[k] = dict(label=k, range=[0, 1], weight=1)

var_ids = list(variables.keys())
var_labels = [v['label'] for v in list(variables.values())]

weight_range = [-1, 1]
ngrid = 5


# pylint: disable=redefined-builtin
def get_controls(id, desc, range, default_weight=0.0):
    """Get controls for one variable.

    This includes
     * the description
     * range 
     * weight
    """
    label = dcc.Input(
        id=id + "_label", type='text', value=desc, className="label")
    range_low = dcc.Input(
        id=id + "_low", type='number', value=range[0], className="range")
    range_high = dcc.Input(
        id=id + "_high", type='number', value=range[1], className="range")
    slider = dcc.Slider(
        id=id + "_weight",
        min=weight_range[0],
        max=weight_range[1],
        value=default_weight,
        step=0.01)
    #grid = dcc.Input(id=id + "_grid", type='number', value=ngrid)
    return html.Tr(
        [
            html.Td(label),
            html.Td([range_low, html.Span('to'), range_high]),
            html.Td([
                html.Span(slider, className="slider"),
                html.Span('', id=id + "_weight_label")
            ])
        ],
        id=id + "_tr")


controls_dict = collections.OrderedDict()
for k, v in list(variables.items()):
    controls = get_controls(k, v['label'], v['range'])
    controls_dict[k] = controls

head_row = html.Tr([
    html.Th('Variable'),
    html.Th('Range'),
    html.Th('Importance'),
])
controls_html = html.Table(
    [head_row] + list(controls_dict.values()), id='controls')
label_states = [
    dash.dependencies.State(k + "_label", 'value') for k in var_ids
]
low_states = [dash.dependencies.State(k + "_low", 'value') for k in var_ids]
high_states = [dash.dependencies.State(k + "_high", 'value') for k in var_ids]
weight_states = [
    dash.dependencies.State(k + "_weight", 'value') for k in var_ids
]

inp_nvars = html.Div([
    html.Span('Number of variables: '),
    dcc.Input(
        id='inp_nvars',
        type='number',
        value=NVARS_DEFAULT,
        max=NVARS_MAX,
        min=1,
        className="nvars range")
])

inp_nsamples = html.Div([
    html.Span('Number of samples: '),
    dcc.Input(
        id='nsamples', type='number', value=10, className="nsamples range")
])

ninps = len(label_states + low_states + high_states + weight_states) + 2

btn_compute = html.Div([
    html.Button('compute', id='btn_compute'),
    html.Div('', id='compute_info')
])

# Creation of dash app
layout = html.Div(
    [
        inp_nvars,
        inp_nsamples,
        controls_html,
        btn_compute,
        #graph, hover_info,
        #click_info
    ],
    id="container",
    # tag for iframe resizer
    **{'data-iframe-height': ''},
)

# Use custom CSS
# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# Callbacks for slider var_ids
for k, v in list(controls_dict.items()):

    @app.callback(
        dash.dependencies.Output(k + '_weight_label', 'children'),
        [dash.dependencies.Input(k + '_weight', 'value')])
    def slider_output(value):
        """Callback for updating slider value"""
        return "{:5.2f}".format(10**value)


# Callbacks to hide unselected variables
for i in range(NVARS_MAX):

    @app.callback(
        dash.dependencies.Output(var_ids[i] + "_tr", 'style'),
        [dash.dependencies.Input('inp_nvars', 'value')])
    def toggle_visibility(nvars, i=i):
        """Callback for setting variable visibility"""
        style = {}

        if i + 1 > nvars:
            style['display'] = 'none'

        return style


states = label_states + low_states + high_states + weight_states
states += [dash.dependencies.State('inp_nvars', 'value')]
states += [dash.dependencies.State('nsamples', 'value')]


@app.callback(
    dash.dependencies.Output('compute_info', 'children'),
    [dash.dependencies.Input('btn_compute', 'n_clicks')], states)
# pylint: disable=unused-argument, unused-variable
def on_compute(n_clicks, *args):
    """Callback for clicking compute button"""
    if n_clicks is None:
        return ''

    if len(args) != ninps:
        raise ValueError("Expected {} arguments".format(ninps))

    # parse arguments
    nsamples = args[-1]
    nvars = args[-2]

    labels = args[:nvars]
    low_vals = np.array([args[i + NVARS_MAX] for i in range(nvars)])
    high_vals = np.array([args[i + 2 * NVARS_MAX] for i in range(nvars)])
    weight_vals = 10**np.array([args[i + 3 * NVARS_MAX] for i in range(nvars)])

    mode = 'maxmin'
    if mode == 'uniform':
        pass
        #samples = uniform.compute(
        #    var_LB=low_vals,
        #    var_UB=high_vals,
        #    num_samples=nsamples,
        #)
        #df = pd.DataFrame(data=samples, columns=labels)
    elif mode == 'maxmin':
        samples = maxmin.compute(
            var_importance=weight_vals,
            var_LB=low_vals,
            var_UB=high_vals,
            num_samples=nsamples,
            ngrids_per_dim=ngrid,
        )
        df = pd.DataFrame(data=samples, columns=labels)

    else:
        raise ValueError("Unknown mode '{}'".format(mode))

    # add column for filling in experiments
    df['Fitness'] = ""

    from .common import generate_table

    table = generate_table(df, download_link=True)
    # Note: this would have to be created beforehand
    #table = dt.DataTable(
    #    rows=df.to_dict('records'),
    #)

    return table
