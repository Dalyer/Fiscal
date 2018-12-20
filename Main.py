# Main.py

"""This is where the magic happens. """

import os
import Transaction
import Category
from datetime import date
import datetime
import xlsxwriter

############## INFORMATION ###################
DEBIT_FILE_NAME = 'debit_test.csv'
CREDIT_FILE_NAME = 'credit_test.csv'
CATEGORY_FILE_NAME = 'categories.txt'
DATE_RANGE = ''
EARLIEST_YEAR = 2015


# open files
dirName = os.getcwd()

debit_file = os.path.join(dirName, DEBIT_FILE_NAME)
credit_file = os.path.join(dirName, CREDIT_FILE_NAME)
categories_file = os.path.join(dirName, CATEGORY_FILE_NAME)

# create a list of all unsorted transactions
debitFile = open(debit_file, encoding='utf-8', mode='r')
creditFile = open(credit_file, encoding='utf-8', mode='r')
unsorted_debit_transactions = debitFile.readlines()
unsorted_credit_transactions = creditFile.readlines()

# close files
debitFile.close()
creditFile.close()


# #######HELPER FUNCTIONS############# #
def convert_string_list_to_int(list):
    new_list = []
    for i in list:
        new_list.append(int(i))
    return new_list


# FUNCTIONS
def get_debit(date_range):
    print("Loading debit transactions...")
    sorted_debit_transactions = []
    for line in unsorted_debit_transactions:
        clean_line = [i.strip() for i in line.split(',')]
        sorted_debit_transactions.append(clean_line)

    # dates are sorted month day year
    sorted_debit_trans_classes = []
    for line in sorted_debit_transactions:
        # find the proper trans_date and format
        temp = convert_string_list_to_int([i.strip() for i in line[0].split('/')])
        trans_date = date(temp[2], temp[0], temp[1])
        if trans_date not in date_range:
            continue
        # find the trans_amount
        trans_description = line[1]
        # find the trans_amount (fix this its terrible)
        if line[2] != '':
            trans_amount = float(line[2])
            trans_type = 'Income'
        else:
            trans_amount = float(line[3])
            trans_type = 'Expense'

        # make transaction and add it to the list
        sorted_debit_trans_classes.append(Transaction.Transaction(trans_description,
                                                                  trans_amount, trans_date, trans_type))

    return sorted_debit_trans_classes


def get_credit(date_range):
    print("Loading credit transactions...")
    sorted_credit_transactions = []
    for line in unsorted_credit_transactions:
        clean_line = [i.strip() for i in line.split(',')]
    sorted_credit_transactions.append(clean_line)
    # dates are sorted month day year
    # mastercard displays, as Item #,Card #,Transaction Date,Posting Date,Transaction Amount,Description
    sorted_credit_trans_classes = []

    for line in sorted_credit_transactions:
        # find the proper trans_date and format
        temp = line[2]
        trans_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:8]))
        if trans_date not in date_range:
            continue
        # find the trans_description
        trans_description = line[5]  # fix this later so that its a proper category class
        # find the trans_amount (fix this its terrible)
        trans_amount = float(line[4])
        if trans_amount >= 0:
            trans_type = 'Expense'
        else:
            trans_type = 'Payment'

        # make transaction and add it to the list
        sorted_credit_trans_classes.append(
            Transaction.Transaction(trans_description, trans_amount, trans_date, trans_type))

    return sorted_credit_trans_classes


# load on initial script start
def load_cat():
    print("Loading categories...")
    categoryFile = open(categories_file, encoding='utf-8', mode='r+')
    categories = []
    for line in categoryFile.readlines():
        categories.append(Category.Category(line))
    categoryFile.close()
    return categories


# function for adding categories into the categories file
def update_cat(cat_arr, new_cat):
    if new_cat in cat_arr:
        print("Category already exists. If you get this message there was a big error\n")
        # TODO replace with a proper error class and handler
    else:
        categoryFile = open(categories_file, encoding='utf-8', mode='r+')
        categoryFile.write("\n" + new_cat)
        categoryFile.close()
        cat_arr.append(new_cat)
        print("New category added")
        return cat_arr


def run():
    print("Starting...")
    all_cat = load_cat()

    # TODO make these loops a get_input function or something
    # ask for start date
    while True:

        # starting date
        print("Enter the starting date for sorting\nUse the form YEAR-MM-DAY")
        date_range = input("> ")
        try:
            #test for proper date forms
            date_range = date_range.split("-")
            input_year = int(date_range[0])
            input_month = int(date_range[1])
            input_day = int(date_range[2])
        except IndexError:
            print("Improper date format used")

        # make sure input year isnt in the future
        if input_year > date.today().year or input_year < EARLIEST_YEAR:
            print("Invalid year")
            continue
        elif input_month > 12 or input_month <= 0:
            print("Invalid month")
            continue
        elif input_day > 31 or input_day < 0:
            print("Invalid day")
            continue
        else:
            start_date = date(input_year, input_month, input_day)
            break

    # end date
    while True:

        # starting date
        print("Enter the end date for sorting\nUse the form YEAR-MM-DAY")
        date_range = input("> ")
        try:
            #test for proper date forms
            date_range = date_range.split("-")
            input_year = int(date_range[0])
            input_month = int(date_range[1])
            input_day = int(date_range[2])
        except IndexError:
            print("Improper date format used")
        # make sure input year isnt in the future
        if input_year > date.today().year or input_year < EARLIEST_YEAR:
            print("Invalid year")
            continue
        elif input_month > 12 or input_month <= 0:
            print("Invalid month")
            continue
        elif input_day > 31 or input_day < 0:
            print("Invalid day")
            continue
        else:
            end_date = date(input_year, input_month, input_day)
            if end_date <= start_date:
                print("End date must be after start date")
                exit()
            break

    generated_date_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days + 1)]
    debit_trans = get_debit(generated_date_range)
    credit_trans = get_credit(generated_date_range)

    all_trans = debit_trans + credit_trans

    # get the category for each transaction
    for transaction in all_trans:
        # check if it is a pre-existing category
        if transaction.description in all_cat:
            print("Category already found automatically")
        else:
            # get user input on what category it should be
            user_input = input("What category should the following "
                               "transaction be filed under: %s\n> " % transaction.description)
            user_input.upper()
            if user_input not in all_cat:
                transaction.category = Category.Category(user_input)
                all_cat = update_cat(all_cat, user_input)
            else:
                print("Added to already existing category")
                transaction.category = Category.Category(user_input)

    print("All transactions categorized")


# make the excel spreadsheet
def get_spreadsheet(trans_all):
    # TODO FINISH THIS with xlsxwriter
    workbook = xlsxwriter.Workbook('test_worksheet.xlsx')   # creates a new excel file if one by that name doesn't exist
    worksheet = workbook.add_worksheet()    # adds a tab
    workbook.close()





# ########TESTS############ #
# x = sorted_credit_trans_classes[0]
# print(x)
# print(x.category)
# print(x.date)

# print(categories[0].name)
# categoryFile.close()
# x = get_credit()
# print(x[0].date)
x = [1, 2, 3]
# run()
get_spreadsheet(x)



# ############## MAIN LOOP ############ #


