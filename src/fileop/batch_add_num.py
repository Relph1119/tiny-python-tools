#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: batch_add_num.py
@time: 2023/7/10 16:48
@project: tiny-python-tools
@desc: 批量给文件添加序号
"""

import os


def batch_add_num(file_dir, clear=False):
    """
    批量修改文件名
    :param clear: 清空之前的处理
    :param file_dir: 文件目录
    """

    total_num_length = len(str(get_total_num(file_dir)))

    index = 0
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            index += 1
            old_file_name = root + os.sep + file_name
            new_file_name = root + os.sep + handle_file_name(file_name, handle_num(index, total_num_length), clear)
            os.rename(old_file_name, new_file_name)
            print(new_file_name)


def get_total_num(file_dir):
    total_num = 0
    for root, dirs, files in os.walk(file_dir):
        for _ in files:
            total_num += 1

    return total_num


def handle_num(index, total_num_length):
    index_length = len(str(index))
    zero_length = total_num_length - index_length
    return "0" * zero_length + str(index)


def handle_file_name(file_name, index, clear):
    if clear:
        return file_name.split("-")[-1]
    else:
        # file_name为AI处理器组合.png
        return index + "-" + file_name


if __name__ == '__main__':
    file_dir = "E:\LearningDisk\Learning_More\算法\华为OD机试算法题"
    batch_add_num(file_dir)
