from typing import List, Union
from pathlib import Path

from pydantic import BaseModel
from pydantic import ValidationError
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from logging import DEBUG
from logconfig import get_logger

logger = get_logger(__name__, __file__, DEBUG)


def read(workbook: Path, max_col: int, model: BaseModel) -> List[dict]:  
    """
    Read and validate data from a single Excel workbook.
    
    Args:
        workbook: Path to Excel workbook
        columns: Number of columns to read
        model: Pydantic model for validation
        
    Returns:
        List of validated data dictionaries
    """    
    # Open Workbook
    # Multiple issue can happen while opening workbook
    # 1. Caller of the function passes wrong parameter
    # 2. File does not exists
    # 3. Valid file does not exists, incorrect format or something
    # 4. File exists and valid, but corrupted, so could not open
    wb = load_workbook(filename=workbook, read_only=True, data_only=True)
    
    
    # Open Worksheet
    # wb.active => is by default set to 0 by openpyxl, and always provides the first sheet
    # So no chance of exception here
    ws = wb.active

    # max_col, even though its more than actual columns, still this will not raise exception
    # but StopIteration may get raised if the excel sheet is empty
    columns = [cell.value for cell in next(ws.iter_rows(max_col=max_col))]
    # If max_col value is given wrong, then lower() will be called on a None object which will be an exception
    # I need the stacktrace here
    keys = ["_".join(column.lower().split()) for column in columns]

    data = []
    for n, row in enumerate(ws.iter_rows(min_row=2, max_col=max_col), start=2):
        record = {key: cell.value for key, cell in zip(keys, row)}

        record = {}
        for key, cell in zip(keys, row):
            # If number of col headers < number of columns in the row => key will be empty and record[key] => exception
            record[key] = cell.value

        # Get Data Row by Row
        # Issues may come with data, which Pydantic is going to handle
        # So use the exception classes given by pydantic library
        try:
            data.append(model(**record).model_dump())
        except Exception as e:
            logger.debug(f'EXCEL FILE: {workbook.stem} ROW: {n} \n Issue: {e}')

    return data


def reads(workbooks: List[Path], columns: int, model: BaseModel) -> List[dict]:
    """Read and validate data from multiple Excel workbooks."""
    data = []

    # caller might send a non iterable object
    for workbook in workbooks:
        # issue in read function
        data.extend(read(workbook, columns, model))
    return data