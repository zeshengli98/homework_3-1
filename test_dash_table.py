from dash import Dash, dash_table
import pandas as pd

df = pd.read_csv('submitted_orders.csv',index_col=0)

app = Dash(__name__)

app.layout = dash_table.DataTable(data=df.to_dict('records'),id="ad",page_size=8,
                                  style_table={'whiteSpace': 'normal','overflowX': 'auto'},
                                  )

if __name__ == '__main__':
    app.run_server(debug=True,port=8052)