from typing import List

from openpyxl import load_workbook

def read(workbook: str, sheet: str, columns: int, model: str) -> List[dict]:
    wb = load_workbook(filename=workbook, read_only=True, data_only=True)
    ws = wb[sheet]

    columns = [cell.value for cell in next(ws.iter_rows(max_col=columns))]
    keys = ["_".join(column.lower().split()) for column in columns]

    data = []
    for n, row in enumerate(ws.iter_rows(min_row=2), start=2):
        record = {key: cell.value for key, cell in zip(keys, row)}
        data.append(model(**record).model_dump())

    return data