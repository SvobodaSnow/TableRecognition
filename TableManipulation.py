from docx import Document
from spire.doc import Table, TableCell


def add_col_word_table(table: Table, document: Document, col_num: int = -1):
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


def add_coll_table(table: [[]], col_num: int = None, content = None):
    if col_num is None:
        for row in table:
            row.append(content)
    else:
        for row in table:
            row.insert(col_num, content)
    return
