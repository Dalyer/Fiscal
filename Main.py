# Main.py

"""This is where the magic happens. """

import os
import Transaction
import Category
from datetime import date
import string

############## INFORMATION ###################
DEBIT_FILE_NAME = 'debit_test.csv'
CREDIT_FILE_NAME = 'credit_test.csv'
DATE_RANGE = ''

# open files
dirName = os.getcwd()

debit_file = os.path.join(dirName, DEBIT_FILE_NAME)
credit_file = os.path.join(dirName, CREDIT_FILE_NAME)

# create a list of all unsorted transactions
unsorted_debit_transactions = (open(debit_file, encoding='utf-8', mode='r')).readlines()
unsorted_credit_transactions = (open(credit_file, encoding='utf-8', mode='r')).readlines()

# dates from datetime work as year, month, day, hour, minute, second

sorted_debit_transactions = []
sorted_credit_transactions = []

# sorting debit transactions
for line in unsorted_debit_transactions:
    clean_line = [i.strip() for i in line.split(',')]
    sorted_debit_transactions.append(clean_line)

# sorting credit transactions
for line in unsorted_credit_transactions:
    clean_line = [i.strip() for i in line.split(',')]
    sorted_credit_transactions.append(clean_line)




#########TESTS#############
# print(unsorted_debit_transactions[0])
print(sorted_debit_transactions[0])
print(sorted_credit_transactions[3])

