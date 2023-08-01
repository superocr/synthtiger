# -*- coding: utf-8 -*-
# @Time : 2023/3/10 14:22
# @Author : JianjinL
# @eMail : jianjinlv@163.com
# @File : process_dict
# @Software : PyCharm
# @Dscription: 用于生成字典文件

import os
import argparse

# 1. 定义命令行解析器对象
parser = argparse.ArgumentParser(description='字典文件生成器')
# 2. 添加命令行参数
parser.add_argument('--charsets_txt_path', type=str, required=True, help="包含所有可能用到字符的txt文件路径")
parser.add_argument('--dictionary_txt_path', type=str, required=True, help="生成的字典文件路劲")
# 3. 从命令行中结构化解析参数
args = parser.parse_args()
# 原始字符文件
charsets_txt_path = args.charsets_txt_path
# 生成的字典文件
dictionary_txt_path = args.dictionary_txt_path

print("开始解析文件...")
# 读取所有字符
char_list = []
with open(charsets_txt_path, 'r', encoding="utf8") as f_origin:
    chars = f_origin.read().replace('\n', '')

# 写入字典文件
with open(dictionary_txt_path, 'w', encoding="utf8") as f_dict:
    for char in chars:
        if char not in char_list:
            f_dict.write(char+"\n")
            char_list.append(char)

print(f"字典: {dictionary_txt_path} 已生成!")

