#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: slove.py
@time: 2023/6/13 14:40
@project: tiny-python-tools
@desc: 求解方程组
"""

# 系数矩阵
import numpy as np
from numpy.linalg import solve

a = np.array([[1, -3, 2, -1],
              [-1, 2, 1, 2],
              [2, 1, -1, 1],
              [3, -1, 2, -3]])
# 常数项列矩阵
b = np.array([9, -3, -2, 11]).T
# 方程组的解
x = solve(a, b)
print(x)