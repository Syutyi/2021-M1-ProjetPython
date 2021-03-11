#!/usr/bin/python
import itertools


class Order:
    id_iter = itertools.count()
    
    def __init__(self, quantity, price):
        self.__quantity = quantity
        self.__price = price
        self.__id =  next(self.id_iter) + 1

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
    
    def id(self):
        return self.__id
# A book can have many orders (one to many relation)

class Book:
    def __init__(self, name):
        self.__name = name  # The name of the order book
        self.buy_orders = []  # List of buy orders
        self.sell_orders = []  # List of sell orders
        self.executed = []

    def name(self):  # Getter, since the attribute name is private
        return self.__name
    
    # This function verify whether there are opposite order at the same price
    
    def sort_book(self):
        self.buy_orders.sort()
        self.buy_orders.reverse()
        self.sell_orders.sort()
        self.sell_orders.reverse()
    
    def print_infos(self, sell):
        if(sell):
            print("--- Insert SELL ", self.sell_orders[-1].quantity(), "@", self.sell_orders[-1].price(), " id =", self.sell_orders[-1].id()," on ", self.__name)
        else :
            print("--- Insert BUY ", self.buy_orders[-1].quantity(), "@", self.buy_orders[-1].price(), " id =", self.buy_orders[-1].id()," on ", self.__name)
        self.sort_book()
        
        print("Book on ", self.__name)
        
        for i in range(len(self.sell_orders)):
            print("         SELL ", self.sell_orders[i].quantity(), "@", self.sell_orders[i].price(), " id =", self.sell_orders[i].id())
        for j in range(len(self.buy_orders)):
            print("         BUY ", self.buy_orders[j].quantity(), "@", self.buy_orders[j].price(), " id =", self.buy_orders[j].id())
        print("------------------------")

    # Inserting into the order book new orders
    def insert_buy(self, quantity, price):
        obj = Order(quantity, price)
        self.buy_orders.append(obj)
        self.print_infos(False)

    def insert_sell(self, quantity, price):
        obj = Order(quantity, price)
        self.sell_orders.append(obj)
        self.print_infos(True)
