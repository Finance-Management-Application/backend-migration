from enum import Enum
from pathlib import Path

from models.income import *
from models.investment import *
from models.expense import Category, SubCategory, Transaction

BASEDIR = Path(__file__).parent.parent.parent / 'data'

class Expense(Enum):
    TRANSACTION = {
        "workbook": BASEDIR.joinpath('expense').joinpath('clothing.xlsx'),
        "sheet": 'Transaction',
        "columns": 15,
        "model": Transaction
    }
    CATEGORY = {
        "workbook": BASEDIR.joinpath('expense').iterdir(),
        "sheet": 'Category',
        "columns": 1,
        "model": Category
    }
    SUB_CATEGORY = {
        "workbook": BASEDIR.joinpath('expense').iterdir(),
        "sheet": 'Sub Category',
        "columns": 2,
        "model": SubCategory
    }

class Income(Enum):
    INCOME = {
        "workbook": BASEDIR.joinpath('income').iterdir(),
        "sheet": 'Income',
        "columns": 2,
        "model": ""
    }

class Investment(Enum):
    INVESTMENT = {
        "workbook": BASEDIR.joinpath('investment').iterdir(),
        "sheet": 'Investment',
        "columns": 2,
        "model": ""
    }