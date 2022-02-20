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
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    dcc.Dropdown(id='dropdown'),

    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value')
])

@app.callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
def clean_data(value):
     # some expensive data processing step
     cleaned_df = slow_processing_step(value)

     # more generally, this line would be
     # json.dumps(cleaned_df)
     return cleaned_df.to_json(date_format='iso', orient='split')

@app.callback(Output('graph', 'figure'), Input('intermediate-value', 'data'))
def update_graph(jsonified_cleaned_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = create_figure(dff)
    return figure

@app.callback(Output('table', 'children'), Input('intermediate-value', 'data'))
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    table = create_table(dff)
    return table


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
