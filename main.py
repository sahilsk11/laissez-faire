from stock_market import StockMarket
from pprint import pprint

if __name__ == "__main__":
  m = StockMarket()

  (result, err) = m.buy_shares("sk", 99, 5)
  if err != None:
    print(err)
  (result, err) = m.sell_shares("sk", 1, 0)
  if err != None:
    print(err)

  pprint(m.get_details())
