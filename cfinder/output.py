import dash_html_components as html
import urllib


def generate_table(dataframe, max_rows=100, download_link=False):
    table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [
            html.Tr([
                html.Td('{:.2f}'.format(dataframe.iloc[i][col]))
                for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])

    if download_link:
        csv_string = dataframe.to_csv(
            index=False, encoding='utf-8', float_format='%.2f')
        link = html.A(
            'Download CSV',
            download="synthesis_conditions.csv",
            href="data:text/csv;charset=utf-8," + urllib.quote(csv_string),
            target="_blank")
        table = [table, link]

    return table
