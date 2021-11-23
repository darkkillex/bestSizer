import pandas
import os
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def create_upload_component():
    return[

        dcc.Upload(html.Button('Upload File')),

        html.Hr(),

        dcc.Upload(html.A('Upload File')),

        html.Hr(),

        dcc.Upload([
            'Drag and Drop or ',
            html.A('Select a File')
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        })
    ]


def app_layout():
    app.layout = html.Div(
        children=create_upload_component()
    )

app_layout()

if __name__ == '__main__':
    app.server.run(debug=False)

