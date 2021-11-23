import base64
import codecs
import datetime

import dash
import io

import pandas as pd
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = None
dfdtypes = None


def create_upload_component():
    return [
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
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
            multiple=True
        ),
        html.Div(id='output-data-upload'),
    ]


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            buffer = io.StringIO()
            df.info(buf=buffer)
            df_info = pd.DataFrame(columns=['DF INFO'], data=buffer.getvalue().split('\n'))

            if df.empty:
                df = df.fillna(method='ffill').fillna(method='bfill')

            if df.isnull().values.any():
                df = df.fillna(method='ffill').fillna(method='bfill')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            if df.empty:
                df = df.fillna(method='ffill').fillna(method='bfill')

            if df.isnull().values.any():
                df = df.fillna(method='ffill').fillna(method='bfill')
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df_info.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_info.columns]
        ),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        if 'csv' not in list_of_names[0]:
            return html.Div(['There was an error processing this file.'])

        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def app_layout():
    app.layout = html.Div(
        children=create_upload_component())


app_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
