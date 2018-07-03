# -*- coding: utf-8 -*-
from __future__ import print_function
import collections

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import numpy as np

from flask import redirect, send_from_directory
import os

# search UI
#style = {"description_width":"220px"}
#layout = ipw.Layout(width="90%")

# variables
variables = collections.OrderedDict([
    ('temperature', dict(label='Temperature', range=[0.0,1000.0], weight=1.0, unit='K')),
    ('temperature2', dict(label='Temperature', range=[0.0,1000.0], weight=2.0, unit='K')),
])
labels = variables.keys()
nq = len(variables)

weight_range = [0, 10]

def get_controls(id, desc, range, default=1.0):
    """Get controls for one variable.

    This includes specifying the description, range and weight.
    """
    range_low = dcc.Input(id=id+"_low", type='number', value=range[0])
    range_high = dcc.Input(id=id+"_high", type='number', value=range[1])
    slider = dcc.Slider(id=id+"_weight", min=weight_range[0], max=weight_range[1], value=1.0, step=0.1)
    return html.Div([html.Span(desc), range_low, range_high, html.Span(slider, className="slider"), html.Span('weight: '), html.Span('', id=id+"_weight_label")])

controls_dict = collections.OrderedDict()
for k,v in variables.iteritems():
    desc = "{} [{}]: ".format(v['label'], v['unit'])
    if not 'default' in v.keys():
        v['default'] = None

    controls = get_controls(k, desc, v['range'], v['default'])
    controls_dict[k] = controls

controls_html = html.Div( list(controls_dict.values()), id='controls' )
low_states = [ dash.dependencies.State(k+"_low",'value') for k in labels ]
high_states = [ dash.dependencies.State(k+"_high",'value') for k in labels ]
weight_states = [ dash.dependencies.State(k+"_weight",'value') for k in labels ]

ninps = len(low_states + high_states + weight_states)

btn_compute = html.Div([html.Button('compute', id='btn_compute'),
    dcc.Markdown('', id='compute_info')])

css = html.Link(
    rel='stylesheet',
    href='/static/style.css'
)

# Creation of dash app
app = dash.Dash()
app.layout = html.Div([css, controls_html, 
    #inputs_html, 
    btn_compute, 
    #graph, hover_info,
    #click_info
    ])


# needed for css
@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

# slider ranges
for k,v in controls_dict.iteritems():
    @app.callback(
            dash.dependencies.Output(k+'_weight_label','children'),
            [dash.dependencies.Input(k+'_weight','value')])
    def slider_output(value):
        return "{}".format(value)

@app.callback(
    #[dash.dependencies.Output('plot_info', 'children'),
    dash.dependencies.Output('compute_info', 'children'),
    [dash.dependencies.Input('btn_compute', 'n_clicks')],
    low_states+high_states+weight_states
    )
def update_output(n_clicks, *args):

    if len(args) != ninps:
        raise ValueError("Expected {} arguments".format(ninps))
    low_vals = { labels[i] : args[i] for i in range(nq) }
    high_vals = { labels[i] : args[i+nq] for i in range(nq) }
    weight_vals = { labels[i] : args[i+2*nq] for i in range(nq) }

    return compute(low_vals, high_vals, weight_vals)

def compute(low_vals, high_vals, weight_vals):
    """Compute most diverse set of inputs.

    :param low_vals: list of lower bounds
    :param high_vals: list of higher bounds
    :param weight_vals: list of weights
    """
    pass

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()
