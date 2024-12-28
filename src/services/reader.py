from typing import List, Tuple, Union
from pathlib import Path

from pydantic import BaseModel
from pydantic import ValidationError
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from logging import DEBUG
from logconfig import get_logger # type: ignore

logger = get_logger(__name__, f'{__file__[:-3]}.log', DEBUG)


def read(workbook: Path, max_col: int, model: BaseModel) -> Tuple[List[dict], int]:  
    if not isinstance(workbook, Path):
        raise TypeError(f'FunctionParameterError: {workbook} must be a {Path} type Object')
    if not isinstance(max_col, int):
        raise TypeError(f'FunctionParameterError: {max_col} must be a {int} type Object')
    if not issubclass(model, BaseModel):
        raise TypeError(f'FunctionParameterError: {model} must be a subclass of {BaseModel} type Object')


    try:
        wb = load_workbook(filename=workbook, read_only=True, data_only=True)
    except FileNotFoundError as e:
        logger.error(f'WorkbookOpeningError: File not found in {workbook} Path')
        raise
    except InvalidFileException as e:
        logger.error(f'WorkbookOpeningError: {workbook.name} seems to be a non-ooxml(not xlsx format in this case) file')
        raise
    except Exception as e:
        logger.error(f'WorkbookOpeningError: Unknown Error in opening {workbook.name}')
        raise
    

    # wb.active => default set to 0 by openpyxl, and always provides the first sheet
    ws = wb.active

    try:
        columns = [cell.value for cell in next(ws.iter_rows(max_col=max_col))]
    except StopIteration as e:
        logger.error(f'Sheet {str(ws)} is Empty')
        raise

    # If max_col value is given wrong, then lower() will be called on a None object which will be an exception
    try:
        keys = ["_".join(column.lower().split()) for column in columns]
    except AttributeError as e:
        logger.error(f'max_col={max_col} parameter value is higher than expected')
        raise

    data = []
    for n, row in enumerate(ws.iter_rows(min_row=2, max_col=max_col), start=2):
        # record = {key: cell.value for key, cell in zip(keys, row)}

        record = {}
        for key, cell in zip(keys, row):
            # case where there are more row cells than headers
            try:
                record[key] = cell.value
            except KeyError as e:
                logger.error(f"Row {n} has more columns than headers")
                raise

        # Get Data Row by Row
        # Issues may come with data, which Pydantic is going to handle
        # So use the exception classes given by pydantic library
        try:
            data.append(model(**record).model_dump())
        except ValidationError as e:
            logger.debug(f'DataError: {workbook.name} Row: {n} \n {e}')

    return data


def reads(workbooks: List[Path], max_col: int, model: BaseModel) -> Tuple[List[dict], int]:
    """Read and validate data from multiple Uniform Excel workbooks, i.e. max_col of each must be same."""

    if isinstance(workbooks, list):
        raise TypeError(f'FunctionParameterError: {workbooks} must be a {list} type Object')
    if not isinstance(max_col, int):
        raise TypeError(f'FunctionParameterError: {max_col} must be a {int} type Object')
    if not issubclass(model, BaseModel):
        raise TypeError(f'FunctionParameterError: {model} must be a subclass of {BaseModel} type Object')

    data, fail_count, success_count = [], 0, 0
    for workbook in workbooks:
        # issue in read function
        try:
            data.extend(read(workbook, max_col, model))
            success_count +=1
        except Exception as e:
            fail_count +=1
            continue
    return data, round(success_count/(success_count+fail_count)*100)
