"""
SynthTIGER
Copyright (c) 2021-present NAVER Corp.
MIT license
"""

import os
import cv2
import json
import math
import random

import numpy as np
from PIL import Image

from synthtiger import components, layers, templates


class Multiline(templates.Template):
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.count = config.get("count", 100)
        self.corpus = components.BaseCorpus(**config.get("corpus", {}))
        self.font = components.BaseFont(**config.get("font", {}))
        self.color = components.RGB(**config.get("color", {}))
        self.layout = components.FlowLayout(**config.get("layout", {}))
        self.background_images = os.listdir("resources/image")
        # 新增使用背景的参数
        self.background = config.get("background", True)

    def process_background_image(self, image):
        """
        为图片增加背景
        Args:
            image: 原始图片

        Returns:
            merge_image: 合并后的图片
        """
        bg_image_path = os.path.join("resources/image", random.choice(self.background_images))
        # 读取背景图片
        bg_image = cv2.imread(bg_image_path)
        # 截取背景图片的一部分
        h, w, c = image.shape
        h_, w_, c_ = bg_image.shape
        radio = math.ceil(max(h/h_, w/w_) * random.uniform(1.3, 3))
        bg_image_reaize = cv2.resize(bg_image, (w_ * radio, h_ * radio))
        start_x = random.randint(0, w_ * radio-w-1)
        start_y = random.randint(0, h_ * radio-h-1)
        cut_image = bg_image_reaize[start_y:start_y+h, start_x:start_x+w]
        # 合并图片和背景
        merge_image = np.minimum(image[:, :, :3], cut_image)
        return merge_image

    def generate(self):
        texts = [self.corpus.data(self.corpus.sample()) for _ in range(self.count)]
        fonts = [self.font.sample() for _ in range(self.count)]
        color = self.color.data(self.color.sample())

        text_group = layers.Group(
            [
                layers.TextLayer(text, color=color, **font)
                for text, font in zip(texts, fonts)
            ]
        )
        self.layout.apply(text_group)

        bg_layer = layers.RectLayer(text_group.size, (255, 255, 255, 255))
        bg_layer.topleft = text_group.topleft

        image = (text_group + bg_layer).output()
        # 添加背景图片
        if self.background:
            merge_image = self.process_background_image(image)
        else:
            merge_image = image
        label = texts
        # 增加返回文本框位置信息
        bbox = []
        for block in text_group.layers:
            bbox.append(block.bbox.tolist())

        data = {
            "image": merge_image,
            "label": label,
            "bbox": bbox,
        }

        return data

    def init_save(self, root):
        os.makedirs(root, exist_ok=True)
        gt_path = os.path.join(root, "gt.txt")
        self.gt_file = open(gt_path, "w", encoding="utf-8")

    def save(self, root, data, idx):
        image = data["image"]
        label = data["label"]
        # 增加返回文本框位置信息
        bbox = data["bbox"]
        # 转换为PaddleOCR格式
        labels = []
        for i in range(len(label)):
            block = {}
            # 文本内容
            block["transcription"] = label[i]
            # 文本位置
            points = [
                [int(bbox[i][0]), int(bbox[i][1])],
                [int(bbox[i][0])+int(bbox[i][2]), int(bbox[i][1])],
                [int(bbox[i][0])+int(bbox[i][2]), int(bbox[i][1])+int(bbox[i][3])],
                [int(bbox[i][0]), int(bbox[i][1])+int(bbox[i][3])],
            ]
            block["points"] = points
            labels.append(block)
        labels = json.dumps(labels, ensure_ascii=False)
        shard = str(idx // 10000)
        image_key = os.path.join("images", shard, f"{idx}.jpg")
        image_path = os.path.join(root, image_key)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image = Image.fromarray(image[..., :3].astype(np.uint8))
        image.save(image_path, quality=30)
        image_path = image_path.replace('\\', '/')
        self.gt_file.write(f"{image_path}\t{labels}\n")

    def end_save(self, root):
        self.gt_file.close()
