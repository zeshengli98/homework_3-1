

from dash import Dash, dcc, html, Input, Output,State
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.DataFrame({
  'student_id' : range(1, 11),
  'score' : [1, 5, 2, 5, 2, 3, 1, 5, 1, 5]
})

app.layout = html.Div([
    html.H4("Select value for endDateTime:"),
    html.Div(
        children=[
            html.P("You may select a specific endDateTime for the call to " + \
                   "fetch_historical_data. If any of the below is left empty, " + \
                   "the current present moment will be used.")
        ],
        style={'width': '365px'}
    ),


    html.Div(
        children = [
            html.Div(
                children = [
                    html.Label('Date:'),
                    dcc.DatePickerSingle(id='edt-date')
                ],
                style = {
                    'display': 'inline-block',
                    'margin-right': '20px',
                }
            ),
            html.Div(
                children = [
                    html.Label('Hour:'),
                    dcc.Dropdown(list(range(24)), id='edt-hour'),
                ],
                style = {
                    'display': 'inline-block',
                    'padding-right': '5px'
                }
            ),
            html.Div(
                children = [
                    html.Label('Minute:'),
                    dcc.Dropdown(list(range(60)), id='edt-minute'),
                ],
                style = {
                    'display': 'inline-block',
                    'padding-right': '5px'
                }
            ),
            html.Div(
                children = [
                    html.Label('Second:'),
                    dcc.Dropdown(list(range(60)), id='edt-second'),
                ],
                style = {'display': 'inline-block'}
            )
        ]
    ),
    html.Div(id = "aaa")
])

@app.callback(Output('aaa', 'children'), Input('edt-date', 'date'))
def clean_data(edt_date):
     return edt_date


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
