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
debitFile = open(debit_file, encoding='utf-8', mode='r')
creditFile = open(credit_file, encoding='utf-8', mode='r')
unsorted_debit_transactions = debitFile.readlines()
unsorted_credit_transactions = creditFile.readlines()
# close files
debitFile.close()
creditFile.close()
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


# credit transactions
# dates are sorted month day year
# mastercard displays, as Item #,Card #,Transaction Date,Posting Date,Transaction Amount,Description
sorted_credit_trans_classes = []
for line in sorted_credit_transactions:
    # find the proper trans_date and format
    temp = line[2]
    trans_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:8]))
    # find the trans_category
    trans_category = line[5]  # fix this later so that its a proper category class
    # find the trans_amount (fix this its terrible)
    trans_amount = float(line[4])
    if trans_amount >= 0:
        trans_type = 'Expense'
    else:
        trans_type = 'Payment'

    # make transaction and add it to the list
    sorted_credit_trans_classes.append(Transaction.Transaction(trans_category, trans_amount, trans_date, trans_type))


# # TODO
# Add the user interface for determining what category a item belongs in
# add a text file that stores all the common categories












#########TESTS#############
x = sorted_credit_trans_classes[0]
print(x)
print(x.category)
print(x.date)


