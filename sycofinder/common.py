# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position,import-error,multiple-imports
from builtins import range  # pylint: disable=redefined-builtin
import urllib.request, urllib.parse, urllib.error
from dash import html
from dash import dash_table as dt
import base64
import io
import pandas as pd

sample_data_link = html.A("sample data", href="../assets/fitness_sample.csv")
upload_hint = html.P([
    "Upload CSV file with experimental parameters and corresponding fitness values (see ",
    sample_data_link, ")."
])


def render_df(df):
    return html.Div([
        dt.DataTable(rows=df.to_dict('records')),
    ])


def generate_table(dataframe, max_rows=100, download_link=False):

    components = []
    if download_link:
        csv_string = dataframe.to_csv(index=False,
                                      encoding='utf-8',
                                      float_format='%.2f')
        link = html.A('Download CSV',
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
    if row_titles[-1].lower() not in ['fitness', 'scores', 'rank']:
        raise ValueError("Last column needs to be 'fitness', got '{}'.".format(
            row_titles[-1]))

    return df.astype(dtype="float64")


def parse_data(content, name, date):
    if content is None:
        return None, None

    try:
        df = parse_contents(content, name, date)
        validate_df(df)
    except ValueError as e:
        return None, html.P(str(e), className="error")

    nrows = len(df)
    fitness = df.iloc[:, -1]
    msg = "Found {} experiments, with fitness from {} to {}.".format(
        nrows, fitness.min(), fitness.max())

    return df.to_json(date_format='iso', orient='split'), html.P(msg)  # pylint: disable=no-member


# styles
HIDE = {'display': 'none'}
SHOW = {}

#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})
