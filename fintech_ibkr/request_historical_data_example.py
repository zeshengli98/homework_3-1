
# This is an example of a test script.
# When you've correctly coded your 'historicalData' override method in
#  synchronous_functions.py, this script should return a dataframe that's
#  ready to be loaded into the candlestick graph constructor.

from ibapi.contract import Contract
from fintech_ibkr import *
import plotly.graph_objects as go

value = "AAPL" # This is what your text input looks like on your app

# Create a contract object
contract = Contract()
contract.symbol = 'TSM220304C00115000'
contract.secType  = 'OPT'
contract.exchange = 'SMART'
contract.currency = 'USD'

# Get your historical data
historical_data = fetch_historical_data(
        contract=contract,
        endDateTime='',
        durationStr='30 D',       # <-- make a reactive input
        barSizeSetting='1 hour',  # <-- make a reactive input
        whatToShow='MIDPOINT',
        useRTH=True               # <-- make a reactive input
    )

# Print it! This should be a dataframe that's ready to go.
print(historical_data)
# fig = go.Figure(
#     data=[
#         go.Candlestick(
#             x=historical_data['date'],
#             open=historical_data['open'],
#             high=historical_data['high'],
#             low=historical_data['low'],
#             close=historical_data['close']
#         )
#     ]
# )
# fig.show()
# This script is an excellent place for scratch work as you figure this out.