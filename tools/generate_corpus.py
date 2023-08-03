# -*- coding: utf-8 -*-
# @Time : 2022/10/11 11:43
# @Author : JianjinL
# @eMail : jianjinlv@163.com
# @File : main
# @Software : PyCharm
# @Dscription: 将从wikiextractor项目获得的语料转换为本项目可使用的语料数据

import os
import re
import tqdm
import json
import random
import argparse
from bs4 import BeautifulSoup

# 定义命令行解析器对象
parser = argparse.ArgumentParser(description='数据格式转换工具')
parser.add_argument('--wikidata_path', type=str, required=True, help="从维基百科下载的文章数据所在路径")
parser.add_argument('--dictionary', type=str, required=True, help="该语言所对应的字典")
parser.add_argument('--output', type=str, required=True, help="输出语料存放路径")
parser.add_argument('--data_expansion_factor', type=int, required=False, default=1, help="语料扩充倍数,在生成语料不足的情况下可以讲此参数设置大一些")
parser.add_argument('--max_text_length', type=int, required=False, default=25, help="最大文本长度")

# 解析参数
args = parser.parse_args()
wikidata_path = args.wikidata_path
dictionary = args.dictionary
output = args.output
data_expansion_factor = args.data_expansion_factor
max_text_length = args.max_text_length

# 创建输出文件夹
try:
    if os.path.exists(output):
        print(f"Directory '{output}' already exists.")
    else:
        os.makedirs(output)
        print(f"Directory '{output}' created successfully.")
except OSError as e:
    print(f"Error: {e}")
    
# 读取字典
with open(dictionary, 'r', encoding='utf8') as f:
    dicts = set([char[0] for char in f.readlines()])
    
def check_text(text, dicts):
    """
    检查文本是否每个字符都在字典里
    :param text:
    :param dicts:
    :return:
    """
    flag = True
    # 如果字符串为空则直接返回否
    if len(text.replace(" ", "")) == 0:
        flag = False
        return flag
    # 检查文本是否每个字符都在字典里
    for char in text:
        if char not in dicts:
            flag = False
            return flag
    return flag

def write_text(file_, text_):
    """
    将文本写入文件
    :param file: 文件
    :param text: 文本
    :return:
    """
    # 去除字符串首尾空格,并合并多个空格为一个空格
    text_ = re.sub(r"\s+", " ", text_).strip()
    if 1 < len(text_) <= max_text_length:
        file_.write(text_ + "\n")

    
# 将数据写入输出文件夹中，结果分为训练预料(train.txt)和测试语料(test.txt)两个语料文件
with open(os.path.join(output, "train.txt"), 'w', encoding='utf8') as ftrain:
    with open(os.path.join(output, "test.txt"), 'w', encoding='utf8') as ftest:
        # 读取维基百科语料
        for file in os.listdir(wikidata_path):
            with open(os.path.join(wikidata_path, file), 'r', encoding='utf8') as fr:
                for line in tqdm.tqdm(fr.readlines()*int(data_expansion_factor)):
                    data = json.loads(line)
                    for key in ("text", "title"):
                        soup = BeautifulSoup(data[key])
                        # 获取文本内容并按照空格分割为词的列表
                        content = soup.text.replace("\n", " ")
                        word_list = content.split(" ")
                        # 拼凑语料短语
                        text_length = 0
                        text_list = []
                        for index, word in enumerate(word_list):
                            text_length += len(word) + 1
                            text_list.append(word)
                            # 取一个随机数
                            rand_num = random.random()
                            # 百分九十写入训练集，百分十写入测试集
                            if random.random() > 0.9:
                                file_ = ftest
                            else:
                                file_ = ftrain
                            # 写入结果
                            if text_length > int(max_text_length) and len(text_list)>1:
                                text = " ".join(text_list[:-1])
                            elif rand_num > 0.98 and len(text_list) > 1:
                                text = " ".join(text_list)
                            else:
                                continue
                            if check_text(text, dicts) is True:
                                write_text(file_, text)
                            text_length = 0
                            text_list = []