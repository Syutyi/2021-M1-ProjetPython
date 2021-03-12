#!/usr/bin/python
import itertools


class Order:
    # ID That would be incremented at each iteration
    __id_iter = itertools.count()
    
    def __init__(self, quantity, price):
        self.__quantity = quantity
        self.__price = price
        self.__id =  next(self.__id_iter) + 1
        # each order has it own id, and the id increments for each new order that is created

    # The attributes are private here

    def __eq__(self, other):
        return other and self.__quantity == other.__quantity and self.__price == other.__price
        # Return, if the other object exists, whether the price and the quantity are equal

    def __lt__(self, other):
        return other and self.__price < other.__price
        # Return, if the other object exists, whether the price of the current object is lower than the price of the other one

    # The three following are getters since the attributesare private
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
        self.buy_orders.sort()      # Sorting the list by price (since we have defined the __lt__ function for the orders, it can be used)
        self.buy_orders.reverse()   # Reversing the list (since we want the orders that have a higher price first)
        self.sell_orders.sort()     # Same
        self.sell_orders.reverse()  # Same
    
    def print_infos(self, sell):
        # Printing the last element that has been added the list (the new order that has been inserted)
        if(sell):
            print("--- Insert SELL ", self.sell_orders[-1].quantity(), "@", self.sell_orders[-1].price(), " id =", self.sell_orders[-1].id()," on ", self.__name)
        else :
            print("--- Insert BUY ", self.buy_orders[-1].quantity(), "@", self.buy_orders[-1].price(), " id =", self.buy_orders[-1].id()," on ", self.__name)
        # Sorting the order book at each step
        self.sort_book()
        
        # Printing the orders that have been inserted in the book
        print("Book on ", self.__name)
        
        # Printing the sell orders first
        for i in range(len(self.sell_orders)):
            print("         SELL ", self.sell_orders[i].quantity(), "@", self.sell_orders[i].price(), " id =", self.sell_orders[i].id())
        
        # Printing the buy orders
        for j in range(len(self.buy_orders)):
            print("         BUY ", self.buy_orders[j].quantity(), "@", self.buy_orders[j].price(), " id =", self.buy_orders[j].id())
        print("------------------------")

    # Inserting into the order book new orders
    def insert_buy(self, quantity, price):
        # Creating the order
        obj = Order(quantity, price)
        # Adding it to the list
        self.buy_orders.append(obj)
        # Printing the information (False => Buy order / True => Sell order)
        self.print_infos(False)

    def insert_sell(self, quantity, price):
        # Creating the order
        obj = Order(quantity, price)
        # Adding it to the list
        self.sell_orders.append(obj)
        # Printing the information (False => Buy order / True => Sell order)
        self.print_infos(True)
