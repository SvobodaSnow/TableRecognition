from typing import overload

from docx import Document
from spire.doc import Table, TableCell


def add_col(table: Table, document: Document, col_num: int = -1):
    if col_num == -1:
        for i in range(table.Rows.Count):
            row = table.Rows[i]
            row.AddCell()
    else:
        for i in range(table.Rows.Count):
            row = table.Rows[i]
            cell = TableCell(document)
            row.Cells.Insert(col_num, cell)
    return
