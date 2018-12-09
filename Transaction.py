# Transaction.py
"""The transaction class will have a category, name, price, date, and transaction type."""
import os
import Category


class Transaction:

    def __init__(self, category, amount, date, transaction_type):
        self.category = category
        self.amount = amount
        self.date = date
        self.transaction_type = transaction_type







