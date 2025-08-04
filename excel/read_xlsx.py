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
        col_num = 2
        cur_row = 0
        while cur_row < row_num:
            cur_row += 1
            tmp = []
            cur_col = 0
            while cur_col < col_num:
                col_value = work_sheet.cell_value(cur_row, cur_col)  # 当前所在行的某列的值(即定位到一个单元格)
                cur_col += 1
                tmp.append(str(col_value).strip())
            data.append({"address": tmp[0], "value": tmp[1]})
    print("data len:", len(data))
    print(data)

    return data
                

if __name__ == '__main__':
    file_name = 'mintrich-airdrop.xlsx'
    data_list = read_excel(file_name)
    rt = json.dumps({"datas": data_list})
    file_path = 'rich-airdrop-address.json'
    with open(file_path, 'w') as f:
        f.write(rt)
