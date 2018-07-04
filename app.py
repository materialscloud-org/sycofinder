# -*- coding: utf-8 -*-
from __future__ import print_function
import collections

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import uniform

# variables
variables = collections.OrderedDict([
    ('h2o', dict(label='Water', range=[1.0, 6.0], weight=1.0, unit='ml')),
    ('dmf', dict(label='DMF', range=[1.0, 6.0], weight=1.0, unit='ml')),
    ('etoh', dict(label='Ethanol', range=[1.0, 6.0], weight=1.0, unit='ml')),
    ('meoh', dict(label='Methanol', range=[1.0, 6.0], weight=1.0, unit='ml')),
    ('iproh',
     dict(label='Isopropyl alcohol', range=[1.0, 6.0], weight=1.0, unit='ml')),
    ('r_ratio',
     dict(label='Reactants ratio', range=[0.8, 1.8], weight=1.0, unit=None)),
    ('temperature',
     dict(label='Temperature', range=[100.0, 200.0], weight=1.0, unit='C')),
    ('power',
     dict(label='Microwave Power', range=[150.0, 250.0], weight=2.0,
          unit='W')),
    ('time',
     dict(label='Reaction time', range=[2.0, 60.0], weight=2.0, unit='min')),
])
labels = variables.keys()
nq = len(variables)

weight_range = [-1, 1]
grid_points = 5


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [
            html.Tr([
                html.Td('{:.2f}'.format(dataframe.iloc[i][col]))
                for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])


# pylint: disable=redefined-builtin
def get_controls(id, desc, range, default_weight=0.0):
    """Get controls for one variable.

    This includes
     * the description
     * range 
     * weight
    """
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
    #grid = dcc.Input(id=id + "_grid", type='number', value=grid_points)
    return html.Tr([
        html.Td(desc),
        html.Td([range_low, range_high]),
        html.Td([
            html.Span(slider, className="slider"),
            html.Span('', id=id + "_weight_label")
        ])
    ])


controls_dict = collections.OrderedDict()
for k, v in variables.iteritems():
    if v['unit'] is None:
        desc = v['label']
    else:
        desc = "{} [{}]: ".format(v['label'], v['unit'])
    if 'default' not in v.keys():
        v['default'] = None

    controls = get_controls(k, desc, v['range'], v['default'])
    controls_dict[k] = controls

head_row = html.Tr([
    html.Th('Variable'),
    html.Th('Range'),
    html.Th('Weight'),
])
controls_html = html.Table(
    [head_row] + list(controls_dict.values()), id='controls')
low_states = [dash.dependencies.State(k + "_low", 'value') for k in labels]
high_states = [dash.dependencies.State(k + "_high", 'value') for k in labels]
weight_states = [
    dash.dependencies.State(k + "_weight", 'value') for k in labels
]

ninps = len(low_states + high_states + weight_states)

btn_compute = html.Div([
    html.Button('compute', id='btn_compute'),
    html.Div('', id='compute_info')
])

css = html.Link(rel='stylesheet', href='/static/style.css')

# Creation of dash app
app = dash.Dash(__name__, static_folder='static')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.layout = html.Div([
    css,
    controls_html,
    #inputs_html,
    btn_compute,
    #graph, hover_info,
    #click_info
])

# Use custom CSS
# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# Callbacks for slider labels
for k, v in controls_dict.iteritems():

    @app.callback(
        dash.dependencies.Output(k + '_weight_label', 'children'),
        [dash.dependencies.Input(k + '_weight', 'value')])
    def slider_output(value):
        return "{:5.2f}".format(10**value)


@app.callback(
    dash.dependencies.Output('compute_info', 'children'),
    [dash.dependencies.Input('btn_compute', 'n_clicks')],
    low_states + high_states + weight_states)
# pylint: disable=unused-argument
def on_compute(out, *args):
    """Callback for clicking compute button"""

    if len(args) != ninps:
        raise ValueError("Expected {} arguments".format(ninps))

    low_vals = [args[i] for i in range(nq)]
    high_vals = [args[i + nq] for i in range(nq)]
    weight_vals = [args[i + 2 * nq] for i in range(nq)]

    samples = uniform.compute(
        var_importance=weight_vals,
        var_LB=low_vals,
        var_UB=high_vals,
    )
    df = pd.DataFrame(data=samples, columns=labels)
    pd.options.display.float_format = '{:.2f}'.format

    return generate_table(df)

    ## artificially reduce number of variables for speed
    #nvars=3
    #import maxmin
    #return maxmin.compute(
    #        var_importance=weight_vals.values()[:nvars],
    #        var_LB=low_vals.values()[:nvars],
    #        var_UB=high_vals.values()[:nvars],
    #        )


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()
