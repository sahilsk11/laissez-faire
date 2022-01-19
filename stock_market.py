from operator import itemgetter

# laissez-faire is a simple market maker simulator
# we start with a stash of two assets - USD and APPL shares
# APPL shares can be bought with USD and sold for USD

# the objective is to see how the value of each asset
# fluctuates as they are bought and sold

# StockMarket will represent a given marketplace of shares
class StockMarket:
  def __init__(self):
    # initialize the stock market with the IPO
    # of 100 shares at $1 each
    self.open_sell_orders = [
        {
          "offered_by": "APPLE",
          "num_shares": 100,
          "ask_price": 1
        }
      ]
    # initialize with no open buy orders
    self.open_buy_orders = []

    # in this initial market we assume no price has
    # been set yet
    self.price_per_share = None

    # maintain a ledger of all historic transactions
    self.order_book = []

  # when a buyer buys a share, they are providing
  # their own money and we decrease the number of shares
  def buy_shares(self, username, requested_shares, limit_price):
    # our trading algorithm will traverse through
    # open sell orders and find the highest matching
    # offers

    # track the individual orders that comprise
    # the larger transaction
    completed_transactions = []

    # keep track of how many shares were actually bought vs
    # how many the buyer wanted to buy
    outstanding_request_shares = requested_shares

    # assume sell orders are always sorted by
    # ask_price, ascending
    for offer in self.open_sell_orders:
      if outstanding_request_shares > 0 and limit_price >= offer["ask_price"]:
        # there are oustanding shares to buy and offers that match
        purchased_shares = min(outstanding_request_shares, offer["num_shares"])
        offer["num_shares"] -= purchased_shares
        outstanding_request_shares -= purchased_shares
        completed_transactions.append({
          "purchased_from": offer["offered_by"],
          "num_shares": purchased_shares,
          "price": offer["ask_price"]
        })
      self.cleanup_empty_orders()

    # if there are outstanding requested shares that were
    # not able to get bought, add them to the queue of pending
    # buy orders
    if outstanding_request_shares > 0:
      self.open_buy_orders.append({
        "offered_by": username,
        "num_shares": outstanding_request_shares,
        "ask_price": limit_price
      })
      self.open_buy_orders.sort(key=itemgetter("ask_price"), reverse=True)
    
    # construct order details from the transaction
    order_details = {
      "shares_requested": requested_shares,
      "shares_bought": requested_shares - outstanding_request_shares,
      # "average_price": sum([x["price"] for x in completed_transactions]) / len(completed_transactions), # causes divide by 0 if no shares are bought
      "transactions": completed_transactions
    }

    # update order book from the transaction
    for transaction in completed_transactions:
      self.order_book.append({
        "sold_by": transaction["purchased_from"],
        "bought_by": username,
        "num_shares": transaction["num_shares"],
        "price": transaction["price"]
      })

    self.update_price_per_share()

    return order_details, None

  # stock prices are driven ONLY by supply and demand
  # the new price is only the last price paid for the share
  def update_price_per_share(self):
    if len(self.order_book) == 0:
      self.price_per_share = None
      return
    
    self.price_per_share = self.order_book[-1]["price"]

  def sell_shares(self, username, requested_shares, limit_price):
    if self.count_user_shares(username) < requested_shares:
      return (None, "cannot sell more shares than the user owns")

    # our trading algorithm will traverse through
    # open buy orders and find the lowest matching
    # offers

    # track the individual orders that comprise
    # the larger transaction
    completed_transactions = []

    # keep track of how many shares were actually sold vs
    # how many the seller wanted to sell
    outstanding_request_shares = requested_shares

    # assume buy orders are always sorted by
    # ask_price, ascending
    for offer in self.open_buy_orders:
      if outstanding_request_shares > 0 and limit_price <= offer["ask_price"]:
        # there are oustanding shares to sell and offers that match
        sold_shares = min(outstanding_request_shares, offer["num_shares"])
        offer["num_shares"] -= sold_shares
        outstanding_request_shares -= sold_shares
        completed_transactions.append({
          "sold_to": offer["offered_by"],
          "num_shares": sold_shares,
          "price": offer["ask_price"]
        })
    self.cleanup_empty_orders()

    # if there are outstanding requested shares that were
    # not able to get sold, add them to the queue of pending
    # sell orders
    if outstanding_request_shares > 0:
      self.open_sell_orders.append({
        "offered_by": username,
        "num_shares": outstanding_request_shares,
        "ask_price": limit_price
      })
      self.open_sell_orders.sort(key=itemgetter("ask_price"))
    
    # construct order details from the transaction
    order_details = {
      "shares_requested": requested_shares,
      "shares_sold": requested_shares - outstanding_request_shares,
      # "average_price": sum([x["price"] for x in completed_transactions]) / len(completed_transactions),
      "transactions": completed_transactions
    }

    # update order book from the transaction
    for transaction in completed_transactions:
      self.order_book.append({
        "sold_by": username,
        "bought_by": transaction["offered_by"],
        "num_shares": transaction["num_shares"],
        "price": transaction["price"]
      })

    self.update_price_per_share()

    return order_details, None

  def count_user_shares(self, username):
    num_shares = 0
    for order in self.order_book:
      if order["bought_by"] == username:
        num_shares += order["num_shares"]
      elif order["sold_by"] == username:
        num_shares -= order["num_shares"]

    return num_shares


  def get_details(self):
    return {
      "open_buy_orders": self.open_buy_orders,
      "open_sell_orders": self.open_sell_orders,
      "price_per_share": self.price_per_share,
      "order_book": self.order_book
    }

  def cleanup_empty_orders(self):
    i = len(self.open_buy_orders) - 1
    while i >= 0:
      if self.open_buy_orders[i]["num_shares"] == 0:
        self.open_buy_orders.pop(i)
      i -= 1

    i = len(self.open_sell_orders) - 1
    while i >= 0:
      if self.open_sell_orders[i]["num_shares"] == 0:
        self.open_sell_orders.pop(i)
      i -= 1