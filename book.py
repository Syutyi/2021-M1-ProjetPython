#!/usr/bin/python

class Order:
    def __init__(self, quantity, price):
        self.__quantity = quantity
        self.__price = price

    # The attributes are private here

    def __eq__(self, other):
        return other and self.__quantity == other.__quantity and self.__price == other.__price

    # Return, if the other object exists, whether the price and the quantity are equal

    def __lt__(self, other):
        return other and self.__price < other.__price
        # Return, if the other object exists, whether the price of the current object is lower than the price of the

    # other one

    def quantity(self):
        return self.__quantity

    def price(self):
        return self.__price
# A book can have many orders (one to many relation)

class Book:
    def __init__(self, name):
        self.__name = name  # The name of the order book
        self.buy_orders = []  # List of buy orders
        self.sell_orders = []  # List of sell orders

    def name(self):  # Getter, since the attribute name is private
        return self.__name

    # Inserting into the order book new orders
    def insert_buy(self, quantity, price):
        print("BUY")
        obj = Order(quantity, price)
        self.buy_orders.append(obj)

    def insert_sell(self, quantity, price):
        print("SELL")
        obj = Order(quantity, price)
        self.sell_orders.append(obj)
