# Transaction.py
"""The transaction class will have a category, name, price, date, and transaction type."""
import Category


class Transaction:

    def __init__(self, description, amount, date, transaction_type):
        self.description = description
        self.amount = amount
        self.date = date
        self.transaction_type = transaction_type
        self.category = Category.Category







