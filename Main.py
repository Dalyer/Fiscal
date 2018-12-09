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

########HELPER FUNCTIONS##############

def convert_string_list_to_int(list):
    new_list = []
    for i in list:
        new_list.append(int(i))
    return new_list

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

# debit transactions
# dates are sorted month day year
sorted_debit_trans_classes = []
for line in sorted_debit_transactions:
    # find the proper trans_date and format
    temp = convert_string_list_to_int([i.strip() for i in line[0].split('/')])
    trans_date = date(temp[2], temp[0], temp[1])
    # find the trans_amount
    trans_category = line[1]  # fix this later so that its a proper category class
    # find the trans_amount (fix this its terrible)
    if line[2] != '':
        trans_amount = float(line[2])
        trans_type = 'Income'
    else:
        trans_amount = float(line[3])
        trans_type = 'Expense'

    # make transaction and add it to the list
    sorted_debit_trans_classes.append(Transaction.Transaction(trans_category, trans_amount, trans_date, trans_type))












#########TESTS#############
x = sorted_debit_trans_classes[0]
print(x)
print(x.category)
print(x.date)