import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('log')))

from constants.const import Expense
from services.reader import read, reads

# categories = read(**Expense.CATEGORY.value)
# sub_categories = read(**Expense.SUB_CATEGORY.value)
transactions = reads(**Expense.TRANSACTION.value)

print(transactions)