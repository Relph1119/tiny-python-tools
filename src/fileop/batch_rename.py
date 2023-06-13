#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: batch_rename.py
@time: 2023/6/13 13:59
@project: tiny-python-tools
@desc: 批量修改文件名
"""
import os


def batch_rename(file_dir):
    """
    批量修改文件名
    :param file_dir: 文件目录
    """
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            old_file_name = root + os.sep + file_name
            new_file_name = root + os.sep + handle_file_name(file_name)
            os.rename(old_file_name, new_file_name)
            print(new_file_name)


def handle_file_name(file_name):
    # file_name为3-03_data-1080P 60帧-AV1.mp4
    suffix = os.path.splitext(file_name)[-1]
    file_name_list = file_name.split("-")
    del file_name_list[-2:]
    del file_name_list[0]

    new_file_name = "-".join(("-".join(file_name_list)).split("_")) + suffix
    return new_file_name


if __name__ == '__main__':
    file_dir = "E:\LearningDisk\Learning_More\Vue3.0视频教程-李立超（因故停更，抱歉）"
    batch_rename(file_dir)
