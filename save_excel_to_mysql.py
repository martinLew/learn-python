# -*- coding:utf-8 -*-
import xlrd
import MySQLdb
import os
import sys


def main(path):
    """
    打开目录遍历excel文件并存储到mysql
    """
    files = os.listdir(path)
    for file in files:
        save_file(path + '/' + file)
        print(file)


def save_file(file):
    """
    打开excel文件
    """
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(0)
    row_nums = sheet.nrows
    col_nums = sheet.ncols

    page = False  # 是否分几次插入

    data = []
    if row_nums < 2:
        return False
    if col_nums not in [23, 25]:  # 两种excel格式，一个23列，一个25列
        return False

    for rownumber in range(1, row_nums):
        if page is True:
            data = []
        values = sheet.row_values(rownumber)
        values.insert(0, 0)
        if values[1] == '':
            return False

        # 不同形式表格差异处理
        if col_nums == 23:
            values.insert(7, '')
            values.insert(8, '')

        if values[20] == '':
            values[20] == '0000-00-00 00:00:00'
        if values[21] == '':
            values[21] = '0000-00-00 00:00:00'

        data.append(tuple(values))
        totals = len(data)
        page = False
        if totals >= 2000:
            insert(data)
            page = True
            del data

    insert(data)
    return True


def insert(data):
    """
    将excel表格所有数据一次插入到mysql中
    """
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="fahuo", use_unicode=True, charset="utf8")
    c = db.cursor()

    c.executemany(
        """INSERT INTO `order` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        data)
    db.commit()
    db.close()


if __name__ == "__main__":
    path = './exceltest'
    main(path)
