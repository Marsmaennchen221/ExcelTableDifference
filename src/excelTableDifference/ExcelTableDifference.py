import sys

from safeds.data.tabular.containers import Table, Column, Row


def table_contains_row(table: Table, row: Row) -> bool:
    for r in table.to_rows():
        if r == row:
            return True
    return False


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] in ("--help", "-h"):
        print("Usage: python ExcelTableDifference [path_to_table1] [path_to_table2] [path_to_output_file]")
        sys.exit(0)

    table_path1 = sys.argv[1]
    table_path2 = sys.argv[2]
    table_diff_path = sys.argv[3]

    table1 = Table.from_excel_file(table_path1)
    table2 = Table.from_excel_file(table_path2)

    table1_wo_2 = table1.filter_rows(lambda row: not table_contains_row(table2, row))
    table2_wo_1 = table2.filter_rows(lambda row: not table_contains_row(table1, row))

    table1_wo_2 = table1_wo_2.add_column(Column("__table__", ["table1"] * table1_wo_2.number_of_rows))
    table2_wo_1 = table2_wo_1.add_column(Column("__table__", ["table2"] * table2_wo_1.number_of_rows))

    table_diff = table1_wo_2.add_rows(table2_wo_1.to_rows())

    table_diff.to_excel_file(table_diff_path)

    print("Successfully wrote difference into table {0}. There are {1} different rows.".format(table_diff_path,
                                                                                               table_diff.number_of_rows))
