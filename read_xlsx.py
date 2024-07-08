#!/usr/bin/env python
# encoding=utf-8

import xlrd
import json

def read_excel(file_name):
    work_book = xlrd.open_workbook(file_name)  # 打开excel文件
    sheet_names = work_book.sheet_names()   # 取出文件内的所有sheet
    data = []
    for sheet in sheet_names:
        work_sheet = work_book.sheet_by_name(sheet) # 打开当前sheet
        row_num = work_sheet.nrows - 1   # nrows取到的是总行数，但是作为索引取值的时候必须要减1，因为索引是从下标0开始的
        # col_num = work_sheet.ncols - 1   # ncols取到的是总列数，但是作为索引取值的时候必须要减1，因为索引是从下标0开始的
        cur_row = 0
        while cur_row < row_num:
            cur_row += 1
            col_num = 1
            col_value = work_sheet.cell_value(cur_row, col_num)  # 当前所在行的某列的值(即定位到一个单元格)
            data.append(str(col_value).strip())
    print("data len:", len(data))
    print(data[:100])

    return data
                

if __name__ == '__main__':
    file_name = 'Forest_address.xlsx'
    data_list = read_excel(file_name)
    rt = json.dumps({"address": data_list})
    file_path = 'address.json'
    with open(file_path, 'w') as f:
        f.write(rt)
