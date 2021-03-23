#!/usr/bin/python
import itertools
import pandas as pd

class Order:
    # ID That would be incremented at each iteration
    __id_iter = itertools.count()

    # each order has it own id, and the id increments for each new order that is created
    def __init__(self, quantity, price):
        self.__quantity = quantity
        self.__price = price
        self.__id = next(self.__id_iter) + 1

    # The attributes are private here
    def __eq__(self, other):
        return other and self.__quantity == other.__quantity and self.__price == other.__price
        # Return, if the other object exists, whether the price and the quantity are equal

    def __lt__(self, other):
        return other and self.__price <= other.__price
        # Return, if the other object exists, whether the price of the current object is lower than the price of the
        # other one The three following are getters since the attributesare private

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def minimum_quantity(self, other):
        if self.__quantity <= other.__quantity:
            return self.__quantity
        else:
            return other.__quantity  # Return the minimum quantity

    # Getters
    def id(self):
        return self.__id

    def price(self):
        return self.__price

    def quantity(self):
        return self.__quantity


# A book can have many orders (one to many relation)

class Book:
    def __init__(self, name):
        self.__name = name  # The name of the order book
        self.buy_orders = []  # List of buy orders
        self.sell_orders = []  # List of sell orders
        self.executed_price = []  # Price of the executed order
        self.executed_quantity = []  # Quantity that have been traded

    def name(self):  # Getter, since the attribute name is private
        return self.__name

    # This function verify whether there are opposite order at the same price

    def sort_book(self):
        self.buy_orders.sort()  # Sorting the list by price (since we have defined the __lt__ function for the
        # orders, it can be used)
        self.buy_orders.reverse()  # Reversing the list (since we want the orders that have a higher price first)
        self.sell_orders.sort()  # Same

    def executed_Order(self, sell):
        if sell:
            # Looking into the buy orders
            last_sell = self.sell_orders[-1]  # Last element inserted
            for i in range(len(self.buy_orders)):
                min_val = 0  # Storing the minimum quantity
                max_price = 0  # Storing the price at which the order is executed If the current buy order has a greater price than the last order (buy + and sell - => both are happy)
                if not self.buy_orders[i].price() < last_sell.price():
                    max_price = self.buy_orders[i].price()
                    # Storing the minimum quantity between the two orders
                    min_val = last_sell.minimum_quantity(self.buy_orders[i])
                    # When it is executed we remove a certain quantity from the orders
                    self.sell_orders[-1].set_quantity(self.sell_orders[-1].quantity() - min_val)
                    self.buy_orders[i].set_quantity(self.buy_orders[i].quantity() - min_val)

                    if min_val != 0:
                        # Adding the order that have been executed in the list of the executed order
                        self.executed_price.append(max_price)
                        self.executed_quantity.append(min_val)


        else:
            # Looking into the sell orders
            last_buy = self.buy_orders[-1]  # Last element inserted
            for i in range(len(self.sell_orders)):
                min_val = 0  # Storing the minimum quantity
                max_price = 0  # Storing the price at which the order is executed
                # If the current buy order has a greater price than the last order
                if not last_buy.price() < self.sell_orders[i].price():
                    max_price = self.sell_orders[i].price()
                    # Storing the minimum quantity between the two orders
                    min_val = last_buy.minimum_quantity(self.sell_orders[i])
                    self.buy_orders[-1].set_quantity(self.buy_orders[-1].quantity() - min_val)
                    self.sell_orders[i].set_quantity(self.sell_orders[i].quantity() - min_val)

                    if min_val != 0:
                        # Same as line 80
                        self.executed_price.append(max_price)
                        self.executed_quantity.append(min_val)

        new_sell = []  # New list that contain the orders that remain
        new_buy = []  # Same
        for i in range(len(self.buy_orders)):
            if not self.buy_orders[i].quantity() == 0:
                # If the quantity is not equal to zero it means that the order remain unaccomplished
                new_buy.append(self.buy_orders[i])
        self.buy_orders = new_buy

        for j in range(len(self.sell_orders)):
            if not self.sell_orders[j].quantity() == 0:
                # same
                new_sell.append(self.sell_orders[j])
        self.sell_orders = new_sell

    def print_executed(self):
        for i in range(len(self.executed_quantity)):
            print("Execute ", self.executed_quantity[i], " at ", self.executed_price[i], " on ", self.__name)

    def create_dataframe_from_order_list(self, order_list, sell):
        # Contains "SELL" if it is a selling order and "BUY" if not
        action_list = []

        # The list of all the information
        quantity_list = []
        price_list = []
        id_list = []
        name_list = []

        # Creating the lists (with all the data)
        for i in range(len(order_list)):
            if sell:
                action_list.append("SELL")
            else:
                action_list.append("BUY")
            name_list.append(self.__name)
            quantity_list.append(order_list[i].quantity())
            price_list.append(order_list[i].price())
            id_list.append(order_list[i].id())

        # Coverting the lists to a panda dataframe
        data_to_be_converted = {'Book': name_list, 'Action': action_list, 'Quantity': quantity_list,
                                'Price': price_list, 'ID': id_list}
        df = pd.DataFrame(data=data_to_be_converted)
        return df

    def pandas_display(self):
        # Creating a data frame for the buy orders
        buy_df = self.create_dataframe_from_order_list(self.buy_orders, False)
        # Creating a data frame for the sell odrers
        sell_df = self.create_dataframe_from_order_list(self.sell_orders, True)
        print("\n-----------------------------------")
        print("\n  ----- Sell-side dataframe -----")
        if not sell_df.empty:
            print(sell_df)
        else :
            print("\n      The dataframe is empty")
        print("\n  ------ Buy-side dataframe -----")
        if not buy_df.empty:
            print(buy_df)
        else:
            print("       The dataframe is empty")
        print("\n-----------------------------------------------------------")

    def print_infos(self, sell):
        # Printing the last element that has been added the list (the new order that has been inserted)
        if sell:
            print("\n--- Insert SELL ", self.sell_orders[-1].quantity(), "@", self.sell_orders[-1].price(), " id =",
                  self.sell_orders[-1].id(), " on ", self.__name)
            self.executed_Order(True)
        else:
            print("\n--- Insert BUY ", self.buy_orders[-1].quantity(), "@", self.buy_orders[-1].price(), " id =",
                  self.buy_orders[-1].id(), " on ", self.__name)
            self.executed_Order(False)
        # Sorting the order book at each step

        # Printing the executed orders
        self.print_executed()
        self.sort_book()

        # Printing the orders that have been inserted in the book
        print("Book on ", self.__name)

        # Printing the sell orders first
        for i in range(len(self.sell_orders)):
            print("         SELL ", self.sell_orders[i].quantity(), "@", self.sell_orders[i].price(), " id =",
                  self.sell_orders[i].id())
        # Printing the buy orders
        for j in range(len(self.buy_orders)):
            print("         BUY ", self.buy_orders[j].quantity(), "@", self.buy_orders[j].price(), " id =",
                  self.buy_orders[j].id())

        self.pandas_display()

    # Inserting into the order book new orders
    def insert_buy(self, quantity, price):
        # Reinitializing the lists
        self.executed_price = []
        self.executed_quantity = []
        # Creating the order
        obj = Order(quantity, price)
        # Adding it to the list
        self.buy_orders.append(obj)
        # Printing the information (False => Buy order / True => Sell order)
        self.print_infos(False)

    def insert_sell(self, quantity, price):
        # Reinitializing the lists
        self.executed_price = []
        self.executed_quantity = []
        # Creating the order
        obj = Order(quantity, price)
        # Adding it to the list
        self.sell_orders.append(obj)
        # Printing the information (False => Buy order / True => Sell order)
        self.print_infos(True)
