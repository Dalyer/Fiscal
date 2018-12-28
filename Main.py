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
TRANSACTIONS_FILE_NAME = 'all_trans_categorized.txt'
DATE_RANGE = ''
EARLIEST_YEAR = 2015
MONTHS = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug',
          'Sept', 'Oct', 'Nov', 'Dec']


# open files
dirName = os.getcwd()

debit_file = os.path.join(dirName, DEBIT_FILE_NAME)
credit_file = os.path.join(dirName, CREDIT_FILE_NAME)
categories_file = os.path.join(dirName, CATEGORY_FILE_NAME)
all_trans_file = os.path.join(dirName, TRANSACTIONS_FILE_NAME)

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
            trans_type = 'EXPENSE'
        else:
            trans_amount = float(line[3])
            trans_type = 'INCOME'

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
            trans_type = 'EXPENSE'
        else:
            trans_type = 'INCOME'
        trans_amount = abs(trans_amount)
        # make transaction and add it to the list
        sorted_credit_trans_classes.append(
            Transaction.Transaction(trans_description, trans_amount, trans_date, trans_type))

    return sorted_credit_trans_classes


# load on initial script start
def load_cat():
    print("Loading categories...")
    categoryFile = open(categories_file, encoding='utf-8', mode='r')
    categories = []
    for line in categoryFile:
        line = line.rstrip('\r\n')
        categories.append(Category.Category(line))
    categoryFile.close()
    return categories


# function for adding categories into the categories file
def update_cat(cat_arr, new_cat):
    if new_cat in cat_arr:
        print("Category already exists. If you get this message there was a big error\n")
        # TODO replace with a proper error class and handler
    else:
        categoryFile = open(categories_file, encoding='utf-8', mode='a+')
        categoryFile.write(new_cat + "\n")
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
            # test for proper date forms
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
            # test for proper date forms
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
        if transaction.description in all_cat:      # TODO this makes zero sense
            print("Category already found automatically")
        else:
            # get user input on what category it should be
            user_input = input("What category should the following "
                               "transaction be filed under: %s | %s\n> "
                               % (transaction.description, transaction.transaction_type))
            user_input = user_input.upper()
            if user_input not in all_cat:
                transaction.category = Category.Category(user_input)
                all_cat = update_cat(all_cat, user_input)
            else:
                print("Added to already existing category")
                transaction.category = Category.Category(user_input)

    print("All transactions categorized")

    # save all transaction in a text file for easy recovery and testing later
    allTransFile = open(all_trans_file, encoding='utf-8', mode='a+')
    all_trans.sort(key=sort_by_date)
    for transaction in all_trans:
        allTransFile.write(transaction.description + "," + str(transaction.amount) + "," + str(transaction.date) + ","
                           + transaction.transaction_type + "," + transaction.category.name + "\n")
    print("All transactions with categories saved")
    allTransFile.close()

    get_spreadsheet(all_trans, generated_date_range)


def sort_by_date(trans):
    return trans.date


def get_monthly_totals(month_index, all_trans, all_cat):
    cat_total = {}
    for cat in all_cat:
        for trans in all_trans:
            if trans.date.month == month_index and trans.category.name == cat.name:
                if trans.category.name in cat_total.keys():
                    cat_total[trans.category.name] += trans.amount
                else:
                    cat_total[trans.category.name] = trans.amount

    # category totals will appear in the order they are listed in the file
    return cat_total


def cartesian_to_excel(row, col):
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
                , 'Q', 'R']
    cartesian_coords = alpha[col] + str(row + 1)
    return cartesian_coords


# make the excel spreadsheet
def get_spreadsheet(trans_all, date_range):
    # TODO FINISH THIS with xlsxwriter

    print("Generating spreadsheet")
    workbook = xlsxwriter.Workbook('test_worksheet.xlsx')  # creates a new excel file if one by that name doesn't exist
    worksheet = workbook.add_worksheet()    # adds a tab
    all_cat = load_cat()
    all_cat_dict = {}
    for cat in all_cat:
        all_cat_dict[cat] = 0
    num_rows = len(all_cat) + 8     # 8 is the number of extra formatting rows
    num_columns = 14

    # separate all income transactions and expense transactions
    income_trans = []
    expense_trans = []
    for trans in trans_all:
        if trans.transaction_type == 'INCOME':
            income_trans.append(trans)
        elif trans.transaction_type == 'EXPENSE':
            expense_trans.append(trans)
        else:
            print("An error has occurred (get_spreadsheet)")

    # get income_cat
    already_pushed = []
    income_cat = {}
    for trans in income_trans:
        if trans.category.name not in already_pushed:
            income_cat[trans.category.name] = 0
            already_pushed.append(trans.category.name)

    # get expense_cat
    expense_cat = {}
    already_pushed.clear()
    for trans in expense_trans:
        if trans.category.name not in already_pushed:
            expense_cat[trans.category.name] = 0
            already_pushed.append(trans.category.name)

    # get lengths
    len_income = len(income_cat)
    len_expense = len(expense_cat)

    # set column and row widths and heights TODO make this done by indexing by the total number of transactions
    worksheet.set_column('A:A', 18)     # title column
    worksheet.set_column('B:M', 10)     # month columns
    worksheet.set_column('N:O', 15)     # totals and averages

    # Formats for different cell types
    main_title_format = workbook.add_format({'bold': True, 'underline': True, 'font_size': 15})
    date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
    month_format = workbook.add_format({'font_size': 15, 'bg_color': 'B3FF79'})
    income_format = workbook.add_format({'font_size': 11, 'font_color': 'white', 'bg_color': '46C732'})
    income_total_format = workbook.add_format({'bold': True, 'font_size': 11,
                                               'font_color': 'white', 'bg_color': '46C732'})
    expense_format = workbook.add_format({'font_size': 11, 'font_color': 'white', 'bg_color': '1551BA'})
    expense_total_format = workbook.add_format({'font_size': 11, 'font_color': 'white', 'bg_color': 'F5352E'})
    savings_format = workbook.add_format({'font_size': 11, 'font_color': 'white','bg_color': 'F5AC2E'})
    percentage_savings_format = workbook.add_format({'bold': True, 'num_format': '0.00%', 'font_size': 11,
                                                     'font_color': 'white', 'bg_color': '15BA30'})
    category_row_format = workbook.add_format({'font_size': 11})
    money_format = workbook.add_format({'font_size': 11, 'num_format': '0.00'})

    # Title
    worksheet.write('A1', "Finances", main_title_format)
    worksheet.write_datetime('B1', date_range[0], date_format)
    worksheet.write_datetime('C1', date_range[-1], date_format)

    # Months header
    worksheet.write_row('B2', MONTHS, month_format)
    worksheet.write('N2', "Total Yearly", month_format)
    worksheet.write('O2', "Averages", month_format)

    # income header
    worksheet.write('A3', "Income", income_format)
    for i in range(num_columns):
        worksheet.write_blank(2, i + 1, None, income_format)

    # income rows
    index = 0
    print(income_cat)
    for key in income_cat:
        worksheet.write(index + 3, 0, key, category_row_format)
        index += 1
    # income total
    worksheet.write(len_income + 3, 0, "Income Total", income_total_format)

    # expense header
    worksheet.write(len_income + 4, 0, "Expenses", expense_format)
    for i in range(num_columns):
        worksheet.write_blank(len_income, i + 1, None, expense_format)

    # expense rows
    already_pushed.clear()
    index = 0
    for key in expense_cat:
        worksheet.write(index + len_income + 5, 0, key, category_row_format)
        index += 1

    # expense total
    worksheet.write(len_expense + len_income + 5, 0
                    , "Total Expenses", expense_total_format)

    # savings header
    worksheet.write(len_expense + len_income + 6, 0
                    , "Savings", savings_format)

    # percentage savings header
    worksheet.write(len_expense + len_income + 7, 0
                    , "Percent Savings", percentage_savings_format)

    # get monthly category totals
    for month_index in range(1, 12):       # loop month
        month_income = get_monthly_totals(month_index, income_trans, all_cat)
        month_expense = get_monthly_totals(month_index, expense_trans, all_cat)

        # display money on the table TODO sort the categories before displaying them
        num_keys = 0
        for key in month_income:
            worksheet.write(num_keys + 3, month_index, month_income[key], money_format)
            num_keys += 1
        num_keys = 0
        for key in month_expense:
            worksheet.write(num_keys + 3 + len(month_income) + 2, month_index, month_expense[key], money_format)
            num_keys += 1
    # Income totals
    for i in range(1, 15):
        start_income = cartesian_to_excel(2, i)
        end_income = cartesian_to_excel(len_income + 2, i)
        worksheet.write_formula(len_income + 3, i
                                , '=SUM(%s:%s)' % (start_income, end_income), income_total_format)

    # expense totals
    for i in range(1, 15):
        start_expense = cartesian_to_excel(len_income + 4, i)
        end_expense = cartesian_to_excel(len_expense + len_income + 4, i)
        worksheet.write_formula(len_expense + len_income + 5, i
                                , '=SUM(%s:%s)' % (start_expense, end_expense), expense_total_format)

    # savings monthly totals
    for i in range(1, 15):
        income_total_cell = cartesian_to_excel(len_income + 3, i)
        expense_total_cell = cartesian_to_excel(len_expense + len_income + 5
                                                , i)
        worksheet.write_formula(len_expense + len_income + 6, i
                                , '=%s-%s' % (income_total_cell, expense_total_cell), savings_format)

    # percent savings
    for i in range(1, 15):
        income_total_cell = cartesian_to_excel(len_income + 3, i)
        savings_total_cell = cartesian_to_excel(len_expense + len_income + 6
                                                , i)
        worksheet.write_formula(len_expense + len_income + 7, i
                                , '=%s/%s' % (income_total_cell, savings_total_cell), percentage_savings_format)
    # TODO CALCULATE THE MONTHLY YEARLY AVERAGES
    # TODO create the graphs

    # close the workbook
    workbook.close()


# ########TESTS############ #

# # Test data set
test_trans_1 = Transaction.Transaction("Mcdonalds Burger", 5.50, date(2018, 1, 1), "INCOME")
test_trans_2 = Transaction.Transaction("Walmart test crap", 11, date(2018, 1, 2), "INCOME")
test_trans_4 = Transaction.Transaction("Walmart test crap", 11, date(2018, 1, 2), "INCOME")
test_trans_3 = Transaction.Transaction("New shoes!", 78.98, date(2018, 1, 3), "EXPENSE")
test_trans_1.category = Category.Category("FOOD")
test_trans_2.category = Category.Category("TOILETRIES")
test_trans_4.category = Category.Category("TOILETRIES")
test_trans_3.category = Category.Category("CLOTHES")
test_trans_all = [test_trans_1, test_trans_2, test_trans_3, test_trans_4]

test_date_range = [date(2018, 1, 1), date(2018, 1, 2), date(2018, 1, 3)]
get_spreadsheet(test_trans_all, test_date_range)

# run()

# ############## MAIN LOOP ############ #
