# krakenClient
This is an interface for Kraken Spot API using ccxt library for the following basic utils:

1. Get account's balance (USDC, USD, EUR)
2. Get necessary trading params: 
    min_size, price, price_precision,  
    quantity_precision, tick_size  
3. Place market order
4. Get open positions
5. Get filled orders

# Useful links:
1. [Kraken's official documentation](https://docs.kraken.com/rest/)
2. [CCXT](https://github.com/ccxt/ccxt)

# Installation
Python version >= 3.10 is required.  
  
`pip3 install ccxt`

# Usage:
```python

client = KrakenSpot(<KRAKEN_PUBLIC_KEY>, <KRAKEN_SECRET_KEY>)

params = client.get_pair_parameters("BTCUSDT")

market_order = client.market_order("BTCUSDT", "buy", 0.010)

filled_order = client.get_order("BTCUSDT", <ORDER_ID>)

position = client.get_positions("BTCUSDT")
```
