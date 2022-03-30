import dash
import plotly.graph_objects as go
from dash import dcc
from dash import html,dash_table
from dash.dependencies import Input, Output, State
from ibapi.contract import Contract
from ibapi.order import Order
from fintech_ibkr import *

import datetime
import pandas as pd

# Make a Dash app!
app = dash.Dash(__name__)
server = app.server
# Define the layout.
app.layout = html.Div([
    html.Div(
        id='sync-connection-status',
        children='False',
        style={'display': 'none'}
    ),

    # Section title
    html.H3("Section 1: Fetch & Display exchange rate historical data"),
        html.Div([
        html.H4("Select value for whatToShow:"),
        html.Div(
            dcc.Dropdown(
                ["TRADES", "MIDPOINT", "BID", "ASK", "BID_ASK", "ADJUSTED_LAST",
                 "HISTORICAL_VOLATILITY", "OPTION_IMPLIED_VOLATILITY", 'REBATE_RATE',
                 'FEE_RATE', "YIELD_BID", "YIELD_ASK", 'YIELD_BID_ASK', 'YIELD_LAST',
                 "SCHEDULE"],
                "MIDPOINT",
                id='what-to-show'
            ),
            style = {'width': '365px'}
        ),

        # Add a Duration block to make duration reactive
        html.H4("Select value for Duration:"),
        html.Div(
            children = [
                html.P("Set the query duration up to one week, using a time unitof seconds, days or weeks." + \
                       "Duration includes S (seconds), D (days) or W (week)")
            ],
            style = {'width': '365px'}
        ),
        html.Div(
            # The input object itself
            ["Input duration: ", dcc.Input(
                id='duration-Int', value='10', type='text'
            ), dcc.Dropdown(options=[
           {'label': 'Second', 'value': 'S'},
           {'label': 'Day', 'value': 'D'},
           {'label': 'Week', 'value': 'W'},
       ],value = "D",id='duration-type')],
            # Style it so that the submit button appears beside the input.
            style={'width': '365px'}
        ),

        # Add a barSize block to make barSizeSetting var reactive
        html.H4("Select value for barSize:"),
        html.Div(
            children=[
                html.P("Specifies the size of the bars that will be showed in the figure")
            ],
            style={'width': '365px'}
        ),
        html.Div(
            # The input object itself
            ["Select bar size: ", dcc.Dropdown(["1 sec","5 secs","15 secs","30 secs",
                                                "1 min","2 mins","3 mins","5 mins","15 mins",
                                                "30 mins","1 hour","1 day"], "1 hour", id='bar-size')],
            # Style it so that the submit button appears beside the input.
            style={'width': '365px'}
        ),

        html.H4("Select returning data:"),
        html.Div(
            children=[
                html.P("Specifies the size of the bars that will be showed in the figure")
            ],
            style={'width': '365px'}
        ),
        html.Div(
            # The input object itself
            ["Select bar size: ", dcc.RadioItems(options = [{"label":"return all data","value":False},
                                                            {"label":"return regular trading time","value":True}],
                                                 value = True, id='data-return-type')],
            # Style it so that the submit button appears beside the input.
            style={'width': '365px'}
        ),

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

        html.H4("Enter a currency pair:"),
        html.P(
            children=[
                "See the various currency pairs here: ",
                html.A(
                    "currency pairs",
                    href='https://www.interactivebrokers.com/en/index.php?f=2222&exch=ibfxpro&showcategories=FX'
                )
            ]
        ),
        # Currency pair text input, within its own div.
        html.Div(
            # The input object itself
            ["Input Currency: ", dcc.Input(
                id='currency-input', value='AUD.CAD', type='text'
            )],
            # Style it so that the submit button appears beside the input.
            style={'display': 'inline-block', 'padding-top': '5px'}
        ),
            # Submit button
            html.Button('Submit', id='submit-button', n_clicks=0),

            # Line break
            html.Br(),
            # Div to hold the initial instructions and the updated info once submit is pressed
            html.Div(id='currency-output', children='Enter a currency code and press submit',
                     style={'color': 'blue', 'fontSize': 15}),
    ],
        style={'width': '405px', 'display': 'inline-block'}
    ),

    html.Div([
        html.Div([
            html.Div([
                html.H4(
                    'Hostname: ',
                    style={'display': 'inline-block', 'margin-right': 20}
                ),
                dcc.Input(
                    id='host',
                    value='127.0.0.1',
                    type='text',
                    style={'display': 'inline-block'}
                )],
                style={'display': 'inline-block'}
            ),
            html.Div([
                html.H4(
                    'Port: ',
                    style={'display': 'inline-block', 'margin-right': 59}
                ),
                dcc.Input(
                    id='port',
                    value='7497',
                    type='text',
                    style={'display': 'inline-block'}
                )],
                style={'display': 'inline-block'}
            ),
            html.Div([
                html.H4(
                    'Client ID: ',
                    style={'display': 'inline-block', 'margin-right': 27}
                ),
                dcc.Input(
                    id='clientid',
                    value='10645',
                    type='text',
                    style={'display': 'inline-block'}
                )
            ],
                style={'display': 'inline-block'}
            )
        ]
        ),
        html.Br(),
        html.Button('TEST SYNC CONNECTION', id='connect-button', n_clicks=0),
        html.Div(id='connect-indicator'),
        html.Div(id='contract-details')
    ],
        style={'width': '405px', 'display': 'inline-block',
               'vertical-align': 'top', 'padding-left': '15px'}
    ),





    # Div to hold the candlestick graph
    dcc.Loading(
        id="loading-1",
        type="default",
        children=html.Div([dcc.Graph(id='candlestick-graph')])
    ),
    # Another line break
    html.Br(),
    # Section title
    html.H2("Make a Trade"),
    # Div to confirm what trade was made
    # html.Div(id='trade-output'),
    html.Div(id='trade-output', children='Lets make an order',
             style={'color': 'blue', 'fontSize': 20}),
    # Radio items to select buy or sell
    dcc.RadioItems(
        id='buy-or-sell',
        options=[
            {'label': 'BUY', 'value': 'BUY'},
            {'label': 'SELL', 'value': 'SELL'}
        ],
        value='BUY'
    ),
    # # Trade type
    dcc.RadioItems(id='order-type', options=[{'label': 'Market', 'value': 'MKT'},
                                             {'label': "Limit", 'value': 'LMT'}], value='MKT', inline=True),
    html.Div(
        # The input object itself
        ["Limit Price: ", dcc.Input(id='limit-price', value='100', type='number')],
        style={'padding-top': '5px', 'visibility': 'visible'}
    ),

    html.Div(
        # The input object itself
        ["Symbol: ", dcc.Input(id='contract-symbol', value='EUR', type='text')], style={'padding-top': '5px'}
    ),
    html.Div(
        # The input object itself
        ["SerType: ", dcc.Input(id='contract-sec-type', value='CASH', type='text')], style={'padding-top': '5px'}
    ),
    html.Div(
        # The input object itself
        ["Currency: ", dcc.Input(id='contract-currency', value='USD', type='text')], style={'padding-top': '5px'}
    ),
    html.Div(
        # Numeric input for the trade amount
        ["Exchange: ", dcc.Input(id='contract-exchange', value='IDEALPRO', type='text')], style={'padding-top': '5px'}
    ),
    html.Div(
        # Numeric input for the trade amount
        ["Amount: ", dcc.Input(id='trade-amt', value='100', type='number')], style={'padding-top': '5px'}
    ),

    # html.Div(["Input limit price: ", dcc.Input(id='limit-price', value='', type='number')]),
    # Submit button for the trade
    html.Button('Trade', id='trade-button', n_clicks=0),
    html.Div(dash_table.DataTable(data=pd.read_csv('submitted_orders.csv',index_col=0).iloc[::-1].to_dict('records'),
                         id="order-his-table",page_size=10, style_table={'height': '350px'}),
             style = {'width': '800px',})

])
def time_reformat(time):
    t=str(time)
    if len(t)==1:
        t = "0" + t
    return t

@app.callback(
    [
        Output("connect-indicator", "children"),
        Output("sync-connection-status", "children")
    ],
    Input("connect-button", "n_clicks"),
    [State("host", "value"), State("port", "value"), State("clientid", "value")]
)
def update_connect_indicator(n_clicks, host, port, clientid):
    try:
        managed_accounts = fetch_managed_accounts(host, port, clientid)
        message = "Connection successful! Managed accounts: " + ", ".join(
            managed_accounts)
        sync_connection_status = "True"
    except Exception as inst:
        try:
            x, y, z = inst.args
            message = "Error in " + x + ": " + y + ". " + z
        except:
            message = inst
        sync_connection_status = "False"
    return message, sync_connection_status

# Callback for what to do when submit-button is pressed
@app.callback(
    [ # there's more than one output here, so you have to use square brackets to pass it in as an array.
        Output(component_id='currency-output', component_property='children'),
        Output(component_id='candlestick-graph', component_property='figure')
    ],
    Input('submit-button', 'n_clicks'),
    # The callback function will
    # fire when the submit button's n_clicks changes
    # The currency input's value is passed in as a "State" because if the user is typing and the value changes, then
    #   the callback function won't run. But the callback does run because the submit button was pressed, then the value
    #   of 'currency-input' at the time the button was pressed DOES get passed in.
    [State('currency-input', 'value'), State('what-to-show', 'value'),
     State('edt-date', 'date'), State('edt-hour', 'value'),
     State('edt-minute', 'value'), State('edt-second', 'value'),
     State('duration-Int', 'value'),State('duration-type', 'value'), State('bar-size', 'value'),
     State('data-return-type','value'),State('sync-connection-status', 'children'),State('host', 'value'),
     State('port', 'value'),
     State('clientid', 'value') ]
)
def update_candlestick_graph(n_clicks, currency_string, what_to_show,
                             edt_date, edt_hour, edt_minute, edt_second,
                             duration_int,duration_type,bar_size,data_return_type,
                             conn_status,host, port, clientid):
    # n_clicks doesn't
    # get used, we only include it for the dependency.
    if not bool(conn_status):
        return '', go.Figure()


    if any([i is None for i in [edt_date, edt_hour, edt_minute, edt_second]]):
        endDateTime = ''
    else:
        date = "".join(edt_date.split("-"))
        hour = time_reformat(edt_hour)
        min = time_reformat(edt_minute)
        sec = time_reformat(edt_second)

        endDateTime = date + ' '+ hour + ":" + min + ":" + sec

    # First things first -- what currency pair history do you want to fetch?
    # Define it as a contract object!
    contract = Contract()
    contract.symbol   = currency_string.split(".")[0]
    contract.secType  = 'CASH'
    contract.exchange = 'IDEALPRO' # 'IDEALPRO' is the currency exchange.
    contract.currency = currency_string.split(".")[1]

    ############################################################################
    ############################################################################
    # This block is the one you'll need to work on. UN-comment the code in this
    #   section and alter it to fetch & display your currency data!
    # Make the historical data request.
    # Where indicated below, you need to make a REACTIVE INPUT for each one of
    #   the required inputs for req_historical_data().
    # This resource should help a lot: https://dash.plotly.com/dash-core-components

    try:
        contract_details = fetch_contract_details(contract, hostname=host,
                                                  port=int(port), client_id=int(clientid))
    except:
        return ("No contract found for " + currency_string), go.Figure()


    if type(contract_details) == str:
        message = f"Error: {contract_details}! Please check your input."
        # if wrong input, return blank figure
        return message, go.Figure()

    else:
        message = 'Submitted query for ' + currency_string
        # print("sssssss:", str(contract_details))
        # s = str(contract_details).split(",")[10]
        # if  s== currency_string:
        #     message = 'Submitted query for ' + currency_string
        # else:
        #     message = f"Extraction symbol: {s} is not aligned with input {currency_string}."
        #     # if wrong input, return blank figure
        #     return message, go.Figure()

    # Some default values are provided below to help with your testing.
    # Don't forget -- you'll need to update the signature in this callback
    #   function to include your new vars!
    cph = fetch_historical_data(
        contract=contract,
        endDateTime=endDateTime,
        durationStr=f'{duration_int} {duration_type}',       # <-- make a reactive input
        barSizeSetting=bar_size,  # <-- make a reactive input
        whatToShow=what_to_show,
        useRTH=data_return_type               # <-- make a reactive input
    )
    # # # Make the candlestick figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=cph['date'],
                open=cph['open'],
                high=cph['high'],
                low=cph['low'],
                close=cph['close']
            )
        ]
    )
    # # # Give the candlestick figure a title
    fig.update_layout(title=('Exchange Rate: ' + currency_string))
    ############################################################################
    ############################################################################


    # Return your updated text to currency-output, and the figure to candlestick-graph outputs
    return message, fig

# Callback for what to do when trade-button is pressed
@app.callback(
    # We're going to output the result to trade-output
    [Output(component_id='trade-output', component_property='children'),
    Output(component_id='order-his-table', component_property='data')],
    # We only want to run this callback function when the trade-button is pressed
    Input('trade-button', 'n_clicks'),
    # We DON'T want to run this function whenever buy-or-sell, trade-currency, or trade-amt is updated, so we pass those
    #   in as States, not Inputs:
    [State('buy-or-sell', 'value'), State('order-type',"value"),State("limit-price", "value"),State("contract-symbol", "value"),
    State("contract-sec-type", "value"),State("contract-currency", "value"),State("contract-exchange", "value"), State('trade-amt', 'value'),
     State("host", "value"),State("port", "value"), State("clientid", "value")],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    # prevent_initial_call=True
)
def trade(n_clicks, action,order_type,lmt_price, con_symbol, con_type,con_currency, con_exchange, trade_amt,host, port, clientid): # Still don't use n_clicks, but we need the dependency
    table_data = pd.read_csv('submitted_orders.csv',index_col=0).iloc[::-1].to_dict('records')
    if n_clicks==0:
        msg = 'Let\'s make an order!'
        return msg, table_data
    contract = Contract()
    contract.symbol   = con_symbol
    contract.secType  = con_type
    contract.currency = con_currency
    contract.exchange = con_exchange # 'IDEALPRO' is the currency exchange.

    order = Order()
    order.action = action
    order.orderType = order_type
    order.totalQuantity = trade_amt
    order.lmtPrice=lmt_price

    # test for valid contract and order before trading
    matching_symbols = fetch_matching_symbols(con_symbol)
    if matching_symbols.shape[0]==0:
        msg = f"Error: {con_symbol} is not a valid symbol."
        return msg, table_data
    elif con_symbol not in matching_symbols['symbol'].values:
        msg = f"Error: {con_symbol} is not a valid symbol."
        return msg, table_data
    elif con_type not in matching_symbols['sec_type'].values:
        msg = f"Error: {con_type} is not a valid secType."
        return msg, table_data
    elif con_currency not in matching_symbols['currency'].values:
        msg =f"Error: {con_currency} is not a valid currency."
        return msg, table_data


    order_response_mkt = place_order(contract, order)
    con_details = fetch_contract_details(contract)
    time = fetch_current_time(host, port, clientid)
    print("order successful!")
    # Make our trade_order object -- a DICTIONARY.
    trade_order = {
        "timestamp": time,
        "order_id": order_response_mkt['order_id'].iloc[-1],
        "client_id": clientid,
        'perm_id':order_response_mkt['perm_id'].iloc[-1],
        'con_id':con_details['con_id'].iloc[-1],
        'symbol':contract.symbol,
        "action": action,
        "size": trade_amt,
        "order_type": order.orderType,
        "trade_limit": "-" if order.orderType=="MKT" else lmt_price,
        "avg_fill_price":order_response_mkt['avg_fill_price'].iloc[-1],
    }

    try:
        df = pd.read_csv('submitted_orders.csv',index_col=0)
        df = pd.concat([df,pd.DataFrame(trade_order,index = [0])],axis=0,ignore_index=True)
        df.to_csv('submitted_orders.csv')
    except:
        df = pd.DataFrame(trade_order,index = [0])
        df.to_csv('submitted_orders.csv')
    print("order recorded!")
    print("order_response_mkt：",order_response_mkt)
    # Return the message, which goes to the trade-output div's "children" attribute.

    # Make the message that we want to send back to trade-output
    msg = f"{action} {str(trade_amt)} {con_symbol}"

    return msg, df.iloc[::-1].to_dict('records')

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)