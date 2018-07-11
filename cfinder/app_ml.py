# -*- coding: utf-8 -*-
from __future__ import print_function

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from cfinder import app

import plotly.graph_objs as go

from . import ml

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
        # Allow multiple files to be uploaded
        multiple=False),
    #html.Div(id='ml-output-data-upload'),
    html.Div(
        dcc.Graph(id='bar-chart', figure=dict(layout=graph_layout, data=[]))),
    #html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])


@app.callback(
    Output('bar-chart', 'figure'), [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
        Input('upload-data', 'last_modified')
    ])
def update_output(content, name, date):
    if content is None:
        return dict(data=[])

    from common import validate_df, parse_contents

    df = parse_contents(content, name, date)
    validate_df(df)

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
