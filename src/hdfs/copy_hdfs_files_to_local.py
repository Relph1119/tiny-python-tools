#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: test.py
@time: 2021/4/20 20:05
@project: bdp-python-base-components
@desc: 将HDFS文件拷贝到本地
"""
import os

import pyhdfs

if __name__ == '__main__':
    # PROJECT_NAME = 'bdp-python-base-components'
    # root_path = os.path.abspath(os.path.dirname(__file__)).split(PROJECT_NAME)[0]
    # local_path = os.path.join(root_path, PROJECT_NAME, 'test')

    client = pyhdfs.HdfsClient(hosts="10.161.27.67:8020", user_name="nusp")
    path = "/nusp/fileServiceRoot"
    for root, dir, files in client.walk(top=path):
        for file in files:
            print(root, file)
    #         full_path = os.path.join(root, file).replace('\\', '/')
    #         local_file_path = os.path.join(local_path, root)
    #         if not os.path.exists(local_file_path):
    #             os.makedirs(local_file_path)
    #         client.copy_to_local(full_path, os.path.join(local_file_path, file))
    #         print(full_path)

    # local_path = 'D:\\StarCraft II\\SC2Data\\data\\data.002'
    # local_path1 = 'D:\\StarCraft II\\SC2Data\\data\\000000000b.idx'
    #
    # client.copy_from_local(local_path, path + '/test.txt')

    # client.delete(path + '/test.txt')
