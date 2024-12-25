from excel.reader import read
from excel.constants import ExpenseWB

from db import query

categories = read(ExpenseWB.CATEGORY_WS)
sub_categories = read(ExpenseWB.SUB_CATEGORY_WS)
transactions = read(ExpenseWB.TRANSACTION_WS)

print(categories)
print(sub_categories)
print(transactions)

# query.bulk_insert_categories(categories)
# query.bulk_insert_sub_category(sub_categories)
# query.bulk_insert_transactions(personal_transactions, ExpenseWB.PERSONAL)
# query.bulk_insert_transactions(dearness_transactions, ExpenseWB.DEARNESS)