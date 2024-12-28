from typing import List, Tuple, Union
from pathlib import Path

from pydantic import BaseModel
from pydantic import ValidationError
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from logging import DEBUG
from logconfig import get_logger # type: ignore


logger = get_logger(__name__, f'{__file__[:-3]}.log', DEBUG)


def read(workbook: Path, max_col: int, model: BaseModel) -> Tuple[List[dict], dict]:

    if not isinstance(workbook, Path):
        raise TypeError(f'FunctionParameterError: {workbook} must be a {Path} type Object')
    
    if not isinstance(max_col, int):
        raise TypeError(f'FunctionParameterError: max_col must be a {int} type Object')
    elif max_col <=0:
        raise Exception(f'FunctionParameterError: max_col must be a positive integer, got {max_col}')
    
    if not issubclass(model, BaseModel):
        raise TypeError(f'FunctionParameterError: {model} must be a subclass of {BaseModel} type Object')

    try:
        wb = load_workbook(filename=workbook, read_only=True, data_only=True)
    except FileNotFoundError as e:
        logger.error(f'WorkbookError: {workbook.name} : File not found in {workbook} Path')
        raise
    except InvalidFileException as e:
        logger.error(f'WorkbookError: {workbook.name} : Workbook is non-ooxml(not xlsx format in this case) file')
        raise
    except Exception as e:
        logger.error(f'WorkbookError: {workbook.name}: Unknown Error in opening')
        raise
    
    # wb.active => default set to 0 by openpyxl, and always provides the first sheet
    ws = wb.active

    try:
        column_headers = [cell.value for cell in next(ws.iter_rows(max_col=max_col))]
        if not all(column_headers):
            # I should write a custom exception class for this
            raise Exception(f'SchemaError: {workbook.name} : Found empty header cells')
    except StopIteration as e:
        logger.error(f'SheetError: {workbook.name}: {str(ws)} is Empty')
        raise
    else:
        keys = ["_".join(column.lower().split()) for column in column_headers]

    
    data, failure, success = [], 0, 0
    for n, row in enumerate(ws.iter_rows(min_row=2, max_col=max_col), start=2):
        record = {}
        for key, cell in zip(keys, row):
            # case where there are more row cells than headers
            try:
                record[key] = cell.value
            except KeyError as e:
                logger.error(f"SchemaError: {workbook.name} : Row {n} has more columns than headers")
                break
        try:
            data.append(model(**record).model_dump())
            success+=1
        except ValidationError as e:
            logger.debug(f'DataError: {workbook.name} : Row: {n} \n {e}')
            failure+=1
            continue

    return data, {workbook.name: round(success/(success+failure)*100)}


def reads(workbooks: List[Path], max_col: int, model: BaseModel) -> Tuple[List[dict], List[dict]]:

    if not isinstance(workbooks, list):
        raise TypeError(f'FunctionParameterError: {workbooks} must be a {list} type Object')

    data, stats  = [], []
    for workbook in workbooks:
        # issue in read function
        try:
            wb_data, stat = read(workbook, max_col, model)
            data.extend(wb_data)
            stats.append(stat)
        except Exception as e:
            stats.append({workbook.name: 0})
            continue
    return data, stats