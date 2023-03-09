<div align="center">

# SynthTIGER 🐯 : Synthetic Text Image Generator

Synthetic Text Image Generator for OCR Model | [Paper](https://arxiv.org/abs/2107.09313) | [Documentation](https://clovaai.github.io/synthtiger/) | [Datasets](#datasets)

</div>



<img src="https://user-images.githubusercontent.com/12423224/153699080-29da7908-0662-4435-ba27-dd07c3bbb7f2.png"/>

说明文档/[原项目说明](README_EN.md)

# 简介

本项目继承自[synthtiger](https://github.com/superocr/synthtiger)，只要拓展其生成多语言文本检测、文本识别训练数据集的能力。

# 特性

- [x] 支持多行文本生成返回文本框坐标信息
- [x] 支持返回PaddleOCR格式标签
- [x] 支持多行文本生成使用图片作为背景：添加参数background
- [ ] 支持阿拉伯语系
- [ ] 支持西里尔语系
- [ ] 支持元音附标语系

# 安装

```bash
conda create -n synthtiger python=3.7
```

```bash
pip install synthtiger
```

# 使用

## 文本检测

```
synthtiger -o results -w 4 -v examples/multiline/template.py Multiline examples/multiline/config.yaml
```

<img src="./images/det_demo_1.jpg" alt="文本检测样例" style="zoom: 33%;" /><img src="./images/det_demo_2.jpg" alt="文本检测样例" style="zoom: 33%;" />

通过config.yml中的background参数可控制是否使用图片作为背景。

## 文本识别

```
# horizontal
synthtiger -o results -w 4 -v examples/synthtiger/template.py SynthTiger examples/synthtiger/config_horizontal.yaml

# vertical
synthtiger -o results -w 4 -v examples/synthtiger/template.py SynthTiger examples/synthtiger/config_vertical.yaml
```

<img src="./images/rec_demo_1.jpg" alt="文本检测样例" style="zoom: 100%;" />
