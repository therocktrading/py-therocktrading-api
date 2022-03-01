# The Rock Trading Python Library 
*TheRockTrading Python Library to communicate with JSON REST API (current version -> v1)*
# Features
- Official implementation
- Place orders
- Wallet managment 
- Market data


## Installation

pip:
```sh
pip install py-therocktrading-api
```

## Quickstart

Register an account with [The Rock Trading](https://www.therocktrading.com/)
or [The Rock Trading Staging](https://www.staging-therocktrading.com/).

Go to settings page and get the API and APY SECRET keys.
If you want to use the staging set `staging=True`.

```python
from TheRockTrading import Client

trt = Client(API='API', API_SECRET='API_SECRET', staging=False)

trt.currencies()
```

# Examples
- Get orderbook
```python
trt.orderbook('BTCEUR')
```
- Get all tickers
```python
trt.tickers()
```
- Get balance for all coin
```python
trt.balances()
```
- Place an order
```python
#market order
trt.place_order(fund_id='BTCEUR', 
		side='buy', 
		amount='1')
		
#limit order
trt.place_order(fund_id='BTCEUR', 
		side='buy', 
		amount='1', 
		price='60000')

#with a condition es: stop_loss or take_profit
trt.place_order(fund_id='BTCEUR', 
		side='buy', 
		amount='1', 
		price='60000'
		conditional_type='stop_loss',
		conditional_price='55000')
```
- Withdraw
```python
trt.balances(currency='BTCEUR', 
	     destination_address='address'
	     amount=1)
```

You can find the full documentation for the endpoints [here](https://api.therocktrading.com/doc/v1/index.html#api-Account_API-Currency_withdraw_limits)












