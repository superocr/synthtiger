import os
from bidi.algorithm import get_display
import argparse

# 1. 定义命令行解析器对象
parser = argparse.ArgumentParser(description='字典文件生成器')
# 2. 添加命令行参数
parser.add_argument('--label_path', type=str, required=True, help="需要转换的标签路径")
# 3. 从命令行中结构化解析参数
args = parser.parse_args()
# 标签路径
label_path = args.label_path
new_label_path = label_path.replace("gt.txt", "gt_transform.txt")

with open(new_label_path, "w", encoding="utf8") as fw:
    with open(label_path, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            img_path = line.split("\t")[0]
            label = line.split("\t")[1].rstrip()
            # 标签进行bidi转换
            label = get_display(label)
            # 转换后的结果写入新文件中
            fw.write(f"{img_path}\t{label}\n")
print(f"转换完成, 新的标签路径为：{new_label_path}")