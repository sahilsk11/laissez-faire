from stock_market import StockMarket
from pprint import pprint

user_sk = "sk"
user_sd = "sd"

def case1():
  m = StockMarket()

  (result, err) = m.buy_shares(user_sk, 99, 5)
  if err != None:
    print("ERROR: " + err)
  
  (result, err) = m.buy_shares(user_sd, 1, 1)
  if err != None:
    print("ERROR: " + err)

  (result, err) = m.sell_shares(user_sk, 1, 15)
  if err != None:
    print("ERROR: " + err)

  (result, err) = m.buy_shares(user_sd, 1, 20)
  if err != None:
    print("ERROR: " + err)

  pprint(m.get_details())

def case2():
  m = StockMarket()

  (result, err) = m.buy_shares(user_sk, 99, 5)
  if err != None:
    print("ERROR: " + err)
  

  (result, err) = m.sell_shares(user_sk, 1, 15)
  if err != None:
    print("ERROR: " + err)

  (result, err) = m.buy_shares(user_sd, 2, 20)
  if err != None:
    print("ERROR: " + err)

  pprint(m.get_details())



if __name__ == "__main__":
  case2()
  