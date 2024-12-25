from enum import Enum

from .model import Category, SubCategory, Transaction



class Workbook(str, Enum):
    LOCATION = './excel/data/clothing.xlsx'
    TRANSACTION = 'Transaction'
    CATEGORY = 'Category'
    SUB_CATEGORY = 'Sub Category'

WORKBOOK_SHEET_PYDANTIC_MODEL_MAPPING = {
    Workbook.TRANSACTION: Transaction,
    Workbook.CATEGORY: Category,
    Workbook.SUB_CATEGORY: SubCategory,
}