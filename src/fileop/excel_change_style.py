#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: excel_change_style.py
@time: 2024/10/30 13:46
@project: tiny-python-tools
@desc: 考试宝软件试题导入：从一个Excel修改成另一个Excel
"""
import pandas as pd


def read_excel(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)


def handle_data(df, question_type):
    df_items = handle_items(df)
    df_answer = df["答案（填空题用'|'隔开）(必填)"]
    df_question = df["试题题干(必填)"]
    result_df = pd.DataFrame()
    result_df['题干'] = df_question
    result_df['题型'] = question_type
    result_df = pd.concat((result_df, df_items), axis=1)
    result_df['正确答案'] = df_answer
    result_df = result_df.assign(
        解析=pd.NA,
        章节=pd.NA,
        难度=pd.NA
    )
    return result_df


def handle_TorF(df, question_type):
    df_answer = df["答案（填空题用'|'隔开）(必填)"]
    df_question = df["试题题干(必填)"]
    result_df = pd.DataFrame()
    result_df['题干'] = df_question
    result_df['题型'] = question_type
    result_df['正确答案'] = df_answer
    result_df = result_df.assign(
        解析=pd.NA,
        章节=pd.NA,
        难度=pd.NA
    )
    return result_df


def handle_items(df):
    # 处理选项
    df_split = df["选项（用'|'隔开）"].str.split('|', expand=True)
    max_cols = 8
    df_split = df_split.reindex(columns=range(max_cols), fill_value='')
    # 给新列命名
    df_split.columns = ["选项 A", "选项 B", "选项 C", "选项 D", "选项 E", "选项 F", "选项 G",
                        "选项 H"]
    return df_split


def save_excel(df, file_path):
    df.to_excel(file_path, index=False)


# 读取Excel
if __name__ == '__main__':
    file_path = "files/input.xlsx"
    df = read_excel(file_path, "单选")
    df_radio = handle_data(df, question_type="单选题")
    df = read_excel(file_path, "多选")
    df_multi_choices = handle_data(df, question_type="多选题")
    df = read_excel(file_path, "判断")
    df_TorF = handle_TorF(df, question_type="判断题")
    df = pd.concat((df_radio, df_multi_choices, df_TorF), axis=0)
    output_path = "files/output.xlsx"
    save_excel(df, output_path)
