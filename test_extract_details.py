
# This is an example of a test script.
# When you've correctly coded your 'historicalData' override method in
#  synchronous_functions.py, this script should return a dataframe that's
#  ready to be loaded into the candlestick graph constructor.

from ibapi.contract import Contract
from fintech_ibkr import *

value = "EUR.USD" # This is what your text input looks like on your app

# Create a contract object
contract = Contract()
contract.symbol = value.split(".")[0]
contract.secType  = 'CASH'
contract.exchange = 'IDEALPRO'  # 'IDEALPRO' is the currency exchange.
contract.currency = value.split(".")[1]



# create a stock contract
# contract = Contract()
# contract.symbol = 'AAPL'
# contract.secType  = 'OPT'
# contract.exchange = 'SMART'
# contract.currency = 'USD'

host = "127.0.0.1"
port = 7497
clientid = 10645
# Get your contract details
contract_details = fetch_contract_details(contract, hostname=host,
                                                  port=port, client_id=clientid)


print(contract_details['symbol'])
if type(contract_details) == str:
    message = f"Error: {contract_details}! Please check your input."
else:
    s = str(contract_details).split(",")[10]
    if s == value:
        message = 'Submitted query for ' + value
    else:
        message = f"Extraction symbol: {s} is not aligned with input {value}."

print(contract_details)
print(message)
#print(str(contract_details).split(",")[10])
print("Good")
#
# str(contract_details).split(",")[10]
#
# contract_details
#
# print(contract_details)

# This script is an excellent place for scratch work as you figure this out.
