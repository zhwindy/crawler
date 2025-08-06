#!/usr/bin/env python
# encoding=utf-8
import json
import csv
import xlrd


def read_excel(file_path):
    """
    读取excel文件内容
    """
    work_book = xlrd.open_workbook(file_path)  # 打开excel文件
    sheet_names = work_book.sheet_names()   # 取出文件内的所有sheet
    data = []
    for sheet in sheet_names:
        work_sheet = work_book.sheet_by_name(sheet) # 打开当前sheet
        row_num = work_sheet.nrows   # nrows取到的是总行数，但是作为索引取值的时候必须要减1，因为索引是从下标0开始的
        col_num = work_sheet.ncols   # ncols取到的是总列数，但是作为索引取值的时候必须要减1，因为索引是从下标0开始的
        print(f"当前xlsx文档的总行数:{row_num}, 总列数{col_num}")
        cur_row = 0
        while cur_row < row_num:
            tmp = []
            cur_col = 0
            while cur_col < col_num:
                # print(f"当前定位的行数:{cur_row}, 列数{cur_col}")
                col_value = work_sheet.cell_value(cur_row, cur_col)  # 当前所在行的某列的值(即定位到一个单元格)
                cur_col += 1
                tmp.append(str(col_value).strip())
            if not tmp:
                data.append({"value": tmp})
            else:
                data.append(str(tmp[0]))
            cur_row += 1

    print("data len:", len(data))

    return data

def save_to_csv(data):
    """
    保存到csv文件中
    """
    file_path = '/Users/zhaopengfei/Downloads/outlook-mails-100.csv'
    # 将数据写入 CSV 文件
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # 将每个字符串作为单独的一行写入，确保不拆分
        for row in data:
            writer.writerow([row])


if __name__ == '__main__':
    file_path = '/Users/zhaopengfei/Downloads/outlook-mails-100.xls'
    data_list = read_excel(file_path)
    save_to_csv(data_list)
