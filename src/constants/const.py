from enum import Enum
from pathlib import Path

from models.income import *
from models.investment import *
from models.expense import Category, SubCategory, Transaction

BASEDIR = Path(__file__).parent.parent.parent / 'data'

class Expense(Enum):
    TRANSACTION = {
        "workbooks": BASEDIR.joinpath('expense').joinpath('transactions').iterdir(),
        "max_col": 15,
        "model": Transaction
    }
    CATEGORY = {
        "workbook": BASEDIR.joinpath('expense').joinpath('category.xlsx'),
        "max_col": 1,
        "model": Category
    }
    SUB_CATEGORY = {
        "workbook": BASEDIR.joinpath('expense').joinpath('sub_category.xlsx'),
        "max_col": 2,
        "model": SubCategory
    }

class Income(Enum):
    INCOME = {
        "workbook": BASEDIR.joinpath('income').iterdir(),
        "max_col": 2,
        "model": ""
    }

class Investment(Enum):
    INVESTMENT = {
        "workbook": BASEDIR.joinpath('investment').iterdir(),
        "max_col": 2,
        "model": ""
    }