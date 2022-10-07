#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg

import numpy as np
from PIL import Image
#__all__=[Image]


if __name__ == '__main__':  # python入口函数
    input_file = sys.argv[1]  # 获取参数
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)  # 创建文件夹存储图片

    item_dict = {}  # item_dict是字典，{key:value}，key存储图像的名字,value是一行list，存储具体信息
    pen_color = np.zeros(3, np.uint8)  # 创建了有三个元素的一维数组，初始化为0，RGB数组
    width = 0
    height = 0

    with open(input_file, 'r') as fp:
        line = fp.readline()  # 读取每一行命令
        while line:
            line = line.strip().split(' ')  # line是一个list,存储了每一个单词
            if line[0] == 'resetCanvas':
                width = int(line[1])
                height = int(line[2])
                item_dict = {}
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)  # 画布是一个三位数组
                canvas.fill(255)  # 全部设置成白色
                for item_type, p_list, algorithm, color in item_dict.values():
                    if item_type == 'line':
                        pixels = alg.draw_line(p_list, algorithm)  # 函数返回的是像素点坐标列表
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color  # 画布的坐标原点设定
                    elif item_type == 'polygon':
                        pass
                    elif item_type == 'ellipse':
                        pass
                    elif item_type == 'curve':
                        pass
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] == 'drawLine':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]  # 存入item_dict，方便save的时候
            ...

            line = fp.readline()

