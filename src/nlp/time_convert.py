#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: time_convert.py
@time: 2023/10/19 14:21
@project: tiny-python-tools
@desc: 
"""
import json

from time_nlp import TimeNormalizer

tn = TimeNormalizer()
res = tn.parse(target=u"2022年2月23日上午10时40分")
res = json.loads(res)
print(res["timestamp"])
