from enum import Enum

from services.models.income import *
from services.models.investment import *
from services.models.expense import Category, SubCategory, Transaction

class ExpenseWB(str, Enum):
    LOCATION = './data/clothing.xlsx'
    TRANSACTION = 'Transaction'
    CATEGORY = 'Category'
    SUB_CATEGORY = 'Sub Category'

class IncomeWB(str, Enum):
    LOCATION = './data/income.xlsx'

class InvestmentWB(str, Enum):
    LOCATION = './data/investment.xlsx'


EXPENSE_MODEL_MAPPING = {
    ExpenseWB.TRANSACTION: Transaction,
    ExpenseWB.CATEGORY: Category,
    ExpenseWB.SUB_CATEGORY: SubCategory,
}

INCOME_MODEL_MAPPING = {}

INVESTMENT_MODEL_MAPPING = {}