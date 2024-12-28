import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('log')))

from constants.const import Expense
from services.reader import read, reads

# categories, failure = read(**Expense.CATEGORY.value)
# sub_categories = read(**Expense.SUB_CATEGORY.value)
# transactions, volume = reads(**Expense.TRANSACTION.value)


import time
import threading

def sleep():
    print('Sleeping Starts')
    time.sleep(1)
    print('Sleeping End')


start = time.perf_counter()

# threads = []
# for _ in range(10):
#     t = threading.Thread(target=sleep)
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

# for _ in range(5):
#     sleep()



finish = time.perf_counter()

print(round(finish-start, 2))