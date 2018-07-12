# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position,import-error,multiple-imports
from __future__ import print_function
from builtins import range
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import dash_html_components as html
import dash_table_experiments as dt
import base64
import io
import pandas as pd
import numpy as np


def render_df(df):
    return html.Div([
        # Use the DataTable prototype component:
        # github.com/plotly/dash-table-experiments
        dt.DataTable(rows=df.to_dict('records')),
    ])


def generate_table(dataframe, max_rows=100, download_link=False):

    components = []
    if download_link:
        csv_string = dataframe.to_csv(
            index=False, encoding='utf-8', float_format='%.2f')
        link = html.A(
            'Download CSV',
            download="synthesis_conditions.csv",
            href="data:text/csv;charset=utf-8," +
            urllib.parse.quote(csv_string),
            target="_blank",
            className='button')
        components.append(link)

    components.append(
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            # Body
            [
                html.Tr([
                    html.Td(cell_format(dataframe.iloc[i][col]))
                    for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ]))

    return components


def cell_format(value):
    if isinstance(value, float):
        return "{:.2f}".format(value)
    return value


# pylint: disable=unused-variable,unused-argument
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    return df


def validate_df(df):
    row_titles = list(df)
    if row_titles[-1].lower() != 'fitness':
        raise ValueError("Last column needs to be 'fitness', got {}".format(
            row_titles[-1]))

    if not set(df.dtypes.values) < set(
        [np.dtype('float64'), np.dtype('int64')]):
        raise ValueError(
            "All values must be floats, got data tpes\n {}".format(df.dtypes))


# styles
HIDE = {'display': 'none'}
SHOW = {}

#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})
