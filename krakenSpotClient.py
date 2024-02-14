import time, traceback, math
import ccxt


class KrakenSpot():
    """
    This is an interface for Kraken Spot API using ccxt library for the following basic utils:
    1) Get account's balance (USDC, USD, EUR)
    2) Get necessary trading params:
        min_size, price, price_precision, 
        quantity_precision, tick_size
    3) Place market order
    8) Get open positions
    9) Get filled orders

    Useful links:
        https://docs.kraken.com/rest/
        https://github.com/ccxt/ccxt
    """

    def __init__(self, apikey= None, apisecret= None, **kwargs):
        self.client = ccxt.kraken({
            "apiKey": apikey,
            "secret": apisecret,
        })
        self.get_precisions()


    def round_decimals_down(self, number:float, decimals):
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.floor(number)

        factor = 10 ** decimals
        return math.floor(number * factor) / factor
    

    # Get account's balance
    def get_balance(self, coin= "USDC"):
        balance = 0
        try:
            bal = self.client.fetch_balance()['free']
            balance = bal.get(coin, 0)
            
            return({"success": balance})
        except Exception as e:
            ex = f"Error: Get spot balance:\n{traceback.format_exc()}\n"
            print(ex)
            return({"error": ex + str(e)})


    def get_precisions(self):
        try:
            self.markets = self.client.load_markets()

        except Exception as e:
            print(f"Error: Get spot markets:\n{traceback.format_exc()}\n{e}")
    

    # Get usefull parameters for trading pair
    def get_pair_parameters(self, pair= "BTC/USD"):
        try:
            market = self.markets.get(pair, {})

            min_size = market['limits']['amount']['min']
            price = self.client.fetch_ticker(symbol= pair)['close']
            step_size = str(market['precision']['price'])
            price_precision = 0 if len(step_size.split(".")) == 1 else len(step_size.split(".")[1])
            quantity_precision = int(market['info']['lot_decimals'])
            tick_size = float(market['info']['tick_size'])

            params = {
                "min_size": min_size,
                "price": price,
                "price_precision": price_precision,
                "quantity_precision": quantity_precision,
                "tick_size": tick_size
            }
            return(params)
        except Exception as e:
            ex = f"Error: Get pair price:\n{traceback.format_exc()}\n"
            print(ex)
            return({"error": ex + str(e)})
    

    # Execute order
    def make_order(self, pair, side, quantity, market):
        try:
            order = self.client.create_order(symbol= pair, type= market, side= side, amount= quantity)

            if "id" in order:
                time.sleep(0.5)

                amount = quantity
                order_price = 0

                new_order = self.get_order(pair, order['id'])
                if "success" in new_order:
                    amount = new_order['success']['amount']
                    order_price = new_order['success']['price']

                params = {
                    "id": order['id'],
                    "pair": order['symbol'],
                    "side": order['side'],
                    "amount": amount,
                    "price": order_price
                }
                return({"success": params})
            
            else:
                return({"error": order})
        except Exception as e:
            return({"error": str(e)})
    

    # Execute market order
    def market_order(self, pair, side, precized_quantity):
        try:
            """side: ['buy', 'sell']"""
            order = self.make_order(pair, side, precized_quantity, "market")

            return(order)
        except Exception as e:
            ex = f"Error: Place market order:\n{traceback.format_exc()}\n"
            print(ex)
            return({"error": ex + str(e)})
    

    # Get balance for particular pair
    def get_positions(self, pair= "BTC/USD"):
        try:
            symbol = pair
            amount = 0

            coin = pair.split("/")[0]
            bal = self.client.fetch_balance()['free']
            amount = bal.get(coin, 0)

            min_size = -1
            market = self.markets.get(pair, {})

            if "limits" in market:
                min_size = market['limits']['amount']['min']
            
            if amount < min_size and min_size > 0: 
                amount = 0

            params = {
                "pair": symbol,
                "amount": amount,
            }

            return({"success": params})
        except Exception as e:
            ex = f"Error: Get active positions:\n{traceback.format_exc()}\n"
            print(ex)
            return({"error": ex + str(e)})


    # Get a filled order
    def get_order(self, pair, order_id):
        try:
            symbol = pair
            side = "none"
            amount = 0
            price = 0
            
            order = self.client.fetch_order(id= order_id, symbol= pair)

            if order:
                side = order['side'].lower()
                amount = float(order['amount'])
                price = float(order['price'])
            
            params = {
                "pair": symbol,
                "side": side,
                "amount": amount,
                "price": price
            }

            return({"success": params})
        except Exception as e:
            ex = f"Error: Get order:\n{traceback.format_exc()}\n"
            print(ex)
            return({"error": ex + str(e)})

