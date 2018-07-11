# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from cfinder import app

import pandas as pd

from . import ga

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
    html.Div(id='output-data-upload'),
    #html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])


def render_df(df):
    return html.Div([
        # Use the DataTable prototype component:
        # github.com/plotly/dash-table-experiments
        dt.DataTable(rows=df.to_dict('records')),
    ])


@app.callback(
    Output('output-data-upload', 'children'), [
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
    new_pop, variables = ga.main(input_data=df.values, var_names=list(df))
    df_new = pd.DataFrame(new_pop, columns=variables)
    df_new['Fitness'] = ""

    from .common import generate_table
    return generate_table(df_new, download_link=True)
    #return render_df(df_new)


#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})
