import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('log')))

from constants.const import Expense
from services.reader import read, reads

# categories, failure = read(**Expense.CATEGORY.value)
# sub_categories = read(**Expense.SUB_CATEGORY.value)
# transactions, volume = reads(**Expense.TRANSACTION.value)


import time

start = time.perf_counter()

reads(**Expense.TRANSACTION.value)

finish = time.perf_counter()

print(round(finish-start, 2))