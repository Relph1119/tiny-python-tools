#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: text2sql.py
@time: 2025/7/3 10:35
@project: tiny-python-tools
@desc: Text2SQL
"""

import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.openai.openai_chat import OpenAI_Chat


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


loaded = load_dotenv(find_dotenv(), override=True)
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
openai_client = OpenAI(api_key=API_KEY, base_url=BASE_URL, max_retries=3)
vn = MyVanna(client=openai_client, config={'temperature': 0.7, 'model': 'Qwen/Qwen3-8B'})

vn.train(ddl="""
 CREATE TABLE IF NOT EXISTS customers (
   id INT PRIMARY KEY,
   name VARCHAR(100),
   age INT
 )
""")
vn.train(documentation="我们的VIP客户定义为年消费超过10万的客户。")
vn.train(sql="SELECT name, age FROM customers WHERE name = '张三'")
ask = vn.ask("销售额排名前十的客户是谁？")
print(ask)
