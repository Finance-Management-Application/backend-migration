from constants.const import Expense
from services.reader import read

# categories = read(**Expense.CATEGORY.value)
sub_categories = read(**Expense.SUB_CATEGORY.value)
# transactions = read(**Expense.TRANSACTION.value)

print(sub_categories)