from datetime import date as python_builtin_date
from typing import Literal

from pydantic import BaseModel


class Category(BaseModel):
    name: str

class SubCategory(BaseModel):
    name: str
    category_name: str

class Transaction(BaseModel):
    date: python_builtin_date
    
    category : str
    sub_category: str
    
    product_or_service: Literal['Product', 'Service'] | Literal['Missing', 'NA']
    product_or_service_name: str | Literal['Missing']
    brand: str | Literal['Missing', 'NA']
    
    quantity_or_duration: int | Literal['Missing', 'NA']
    unit: str | Literal['Missing', 'NA']
    price: float | Literal['Missing', 'NA']
    platform_or_location: str | Literal['Missing', 'NA']
    need_or_want: Literal['Need', 'Want']
    transaction_mode: Literal['Online', 'Offline'] | None
    
    personal_or_dearness: Literal['Personal', 'Dearness']
    relation: str | None

    details: str | Literal['Missing', 'NA'] | None