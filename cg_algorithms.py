#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(int(y0), int(y1 + 1)):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(int(x0), int(x1 + 1)):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x1 == x0:
            for y in range(int(y0), int(y1 + 1)):
                result.append((x0, y))
        elif y1 == y0:
            for x in range(int(x0), int(x1 + 1)):
                result.append((x, y0))
        else:
            xDis = x1 - x0  # x的增量
            yDis = y1 - y0  # y的增量
            if abs(xDis) > abs(yDis):
                maxstep = abs(xDis)
            else:
                maxstep = abs(yDis)
            xUnitstep = xDis / maxstep  # x每步骤增量
            yUnitstep = yDis / maxstep  # y的每步增量
            x = x0
            y = y0
            for k in range(int(maxstep)):
                x = x + xUnitstep
                y = y + yUnitstep
                result.append((int(x), int(y)))  # 取整操作

    elif algorithm == 'Bresenham':
        if x1 == x0:
            for y in range(int(y0), int(y1 + 1)):
                result.append((x0, y))
                return result
        elif y1 == y0:
            for x in range(int(x0), int(x1 + 1)):
                result.append((x, y0))
                return result
        else:
            k = (y1 - y0) / (x1 - x0)
            if x0 > x1:  # 交换坐标，保证从左到右画线
                x0, y0, x1, y1 = x1, y1, x0, y0

            if k > 1:  # 斜率大于1
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dx - dy
                result.append((x0, y0))
                y = y0
                x = x0
                for y in range(int(y0 + 1), int(y1 + 1)):
                    if p < 0:
                        p += 2 * dx
                        result.append((x, y))
                    else:
                        p += 2 * dx - 2 * dy
                        x += 1
                        result.append((x, y))

            elif k > 0 and k <= 1:  # 斜率为正且小于1
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dy - dx
                result.append((x0, y0))
                y = y0
                x = x0
                for x in range(int(x0 + 1), int(x1 + 1)):
                    if p < 0:
                        p += 2 * dy
                        result.append((x, y))
                    else:
                        p += 2 * dy - 2 * dx
                        y += 1
                        result.append((x, y))

            elif k < 0 and k >= -1:
                y1 = 2 * y0 - y1  # 作对称变换到斜率为正
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dy - dx
                result.append((x0, y0))
                y = y0
                x = x0
                for x in range(int(x0 + 1), int(x1 + 1)):
                    if p < 0:
                        p += 2 * dy
                        result.append((x, 2 * y0 - y))
                        # print(x, y)
                    else:
                        p += 2 * dy - 2 * dx
                        y += 1
                        result.append((x, 2 * y0 - y))  # 再次作对称变换恢复
                        # print(x, y)
            else:
                y1 = 2 * y0 - y1  # 作对称变换到斜率为正
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dx - dy
                result.append((x0, y0))
                y = y0
                x = x0
                for y in range(int(y0 + 1), int(y1 + 1)):
                    if p < 0:
                        p += 2 * dx
                        result.append((x, 2 * y0 - y))  # 再次作对称变换恢复
                        # print(x,y)
                    else:
                        p += 2 * dx - 2 * dy
                        x += 1
                        result.append((x, 2 * y0 - y))
                        # print(x, y)

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)  # 待修改为algorithm
        result += line
    return result


def draw_free(p_list, algorithm):
    """自由绘制

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []

    for i in range(len(p_list) - 2):
        line = draw_line([p_list[i], p_list[i + 1]], algorithm)  # 待修改为algorithm
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []

    x0, y0 = p_list[0]  # 椭圆左上角坐标
    x1, y1 = p_list[1]  # 椭圆右下角坐标
    if x1 < x0:
        d = x0
        x0 = x1
        x1 = d
    if y1 < y0:
        d = y0
        y0 = y1
        y1 = d
    # 获取参数
    a = (x1 - x0) / 2
    b = (y1 - y0) / 2
    # 框架只是一个点或者一个线，绘图
    if a == 0 or b == 0:
        result = draw_line(p_list, 'DDA')
        return result
    # 圆心
    xc = (x1 + x0) / 2
    yc = (y1 + y0) / 2
    # 从点(0,b)开始
    x = 0
    y = b
    d = 4 * b * b - 4 * a * a * b + a * a
    while a * a * (2 * y - 1) >= 2 * (b * b * (x + 1)):
        result.append((x + xc, y + yc))
        result.append((-x + xc, y + yc))
        result.append((x + xc, -y + yc))
        result.append((-x + xc, -y + yc))
        if d < 0:
            d = d + 4 * b * b * (2 * x + 3)
        else:
            d = d + 4 * b * b * (2 * x + 3) - 8 * a * a * (y - 1)
            y = y - 1
        x = x + 1
    result.append((x + xc, y + yc))
    result.append((-x + xc, y + yc))
    result.append((x + xc, -y + yc))
    result.append((-x + xc, -y + yc))
    x = a
    y = 0
    d = 4 * a * a - 4 * a * b * b + b * b
    while 2 * (a * a * (y - 1)) < b * b * (2 * x - 1):
        result.append((x + xc, y + yc))
        result.append((-x + xc, y + yc))
        result.append((x + xc, -y + yc))
        result.append((-x + xc, -y + yc))
        if d < 0:
            d += 4 * a * a * (2 * y + 3)
        else:
            d += 4 * a * a * (2 * y + 3) - 8 * b * b * (x - 1)
            x = x - 1
        y = y + 1
    return result


def draw_curve(p_list, algorithm):  # 存在问题：反应慢
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        BEZIER_SAMPLE_COUNT = 1000
        delta = 1 / BEZIER_SAMPLE_COUNT
        t = 0
        while t <= 1:
            t = t + delta
            list = p_list
            # 只剩一个点即是曲线上的点
            while len(list) > 1:
                tmp = []
                for i in range(len(list) - 1):
                    x1, y1 = list[i]
                    x2, y2 = list[i + 1]
                    tmp.append((t * x1 + (1 - t) * x2, t * y1 + (1 - t) * y2))
                list = tmp
            result += list
    else:
        n = len(p_list)
        k = 4
        u = k - 1
        while (u < n + 1):
            x, y = 0, 0
            # calc P(u)
            for i in range(0, n):
                B_ik = deBoor_Cox(u, k, i)
                x += B_ik * p_list[i][0]
                y += B_ik * p_list[i][1]
            result.append((int(x + 0.5), int(y + 0.5)))
            u += 1 / 20927  # 2020/09/27

    return result


def deBoor_Cox(u, k, i):  # 补充b-spline
    if k == 1:
        if i <= u and u <= i + 1:
            return 1
        else:
            return 0
    else:
        coef_1, coef_2 = 0, 0
        if (u - i == 0) and (i + k - 1 - i == 0):
            coef_1 = 0
        else:
            coef_1 = (u - i) / (i + k - 1 - i)
        if (i + k - u == 0) and (i + k - i - 1 == 0):
            coef_2 = 0
        else:
            coef_2 = (i + k - u) / (i + k - i - 1)
    return coef_1 * deBoor_Cox(u, k - 1, i) + coef_2 * deBoor_Cox(u, k - 1, i + 1)


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for p in p_list:
        p[0] += dx
        p[1] += dy
    return p_list


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for p in p_list:
        a = p[0] - x
        b = p[1] - y
        r = r * math.pi / 180  # 角度转弧度
        p[0] = a * math.cos(r) - b * math.sin(r) + x
        p[1] = a * math.sin(r) + b * math.cos(r) + y

    return p_list


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for p in p_list:
        p[0] = s * p[0] + (1 - s) * x
        p[1] = s * p[1] + (1 - s) * y
    return p_list


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    # ！！需要按照pyqt的坐标轴修改！！
    if algorithm == 'Cohen-Sutherland':
        # Defining region codes
        INSIDE = 0  # 0000
        LEFT = 1  # 0001
        RIGHT = 2  # 0010
        BOTTOM = 4  # 0100
        TOP = 8  # 1000

        x0, y0 = p_list[0]  # 线段左端坐标
        x1, y1 = p_list[1]  # 线段右端坐标

        # Function to compute region code for a point(x, y)
        code1 = INSIDE
        if x0 < x_min:  # to the left of rectangle
            code1 |= LEFT
        elif x0 > x_max:  # to the right of rectangle
            code1 |= RIGHT
        if y0 < y_min:  # below the rectangle
            code1 |= BOTTOM
        elif y0 > y_max:  # above the rectangle
            code1 |= TOP

        code2 = INSIDE
        if x1 < x_min:  # to the left of rectangle
            code2 |= LEFT
        elif x1 > x_max:  # to the right of rectangle
            code2 |= RIGHT
        if y1 < y_min:  # below the rectangle
            code2 |= BOTTOM
        elif y1 > y_max:  # above the rectangle
            code2 |= TOP

        # Clipping a line from P1 = (x0, y0) to P2 = (x1, y1)
        while True:
            # If both endpoints lie within rectangle
            if code1 == 0 and code2 == 0:
                result = [[x0, y0], [x1, y1]]
                break

            # If both endpoints are outside rectangle
            elif (code1 & code2) != 0:
                result = []
                #print('here')
                break

            # Some segment lies within the rectangle
            else:

                # Line Needs clipping
                # At least one of the points is outside,
                # select it
                x = 1.0
                y = 1.0
                if code1 != 0:
                    code_out = code1
                else:
                    code_out = code2

                # Find intersection point
                # using formulas y = y1 + slope * (x - x1),
                # x = x1 + (1 / slope) * (y - y1)
                if code_out & TOP:
                    # point is above the clip rectangle
                    x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                    y = y_max
                elif code_out & BOTTOM:
                    # point is below the clip rectangle
                    x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                    y = y_min
                elif code_out & RIGHT:
                    # point is to the right of the clip rectangle
                    y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                    x = x_max
                elif code_out & LEFT:
                    # point is to the left of the clip rectangle
                    y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                    x = x_min

                # Now intersection point x, y is found
                # We replace point outside clipping rectangle
                # by intersection point
                if code_out == code1:
                    x0 = x
                    y0 = y
                    code1 = INSIDE
                    if x0 < x_min:  # to the left of rectangle
                        code1 |= LEFT
                    elif x0 > x_max:  # to the right of rectangle
                        code1 |= RIGHT
                    if y0 < y_min:  # below the rectangle
                        code1 |= BOTTOM
                    elif y0 > y_max:  # above the rectangle
                        code1 |= TOP
                else:
                    x1 = x
                    y1 = y
                    code2 = INSIDE
                    if x1 < x_min:  # to the left of rectangle
                        code2 |= LEFT
                    elif x1 > x_max:  # to the right of rectangle
                        code2 |= RIGHT
                    if y1 < y_min:  # below the rectangle
                        code2 |= BOTTOM
                    elif y1 > y_max:  # above the rectangle
                        code2 |= TOP
    else:
        if y_min > y_max:
            y_min, y_max = y_max, y_min
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]

        p = [x0 - x1, x1 - x0, y0 - y1, y1 - y0]
        q = [x0 - x_min, x_max - x0, y0 - y_min, y_max - y0]
        u0, u1 = 0, 1

        for i in range(4):
            if p[i] < 0:
                u0 = max(u0, q[i] / p[i])
            elif p[i] > 0:
                u1 = min(u1, q[i] / p[i])
            elif (p[i] == 0 and q[i] < 0):
                result = [[0, 0], [0, 0]]
                return result
            if u0 > u1:
                result = [[0, 0], [0, 0]]
                return result
        res_x0=0
        res_y0=0
        res_x1=0
        res_y1 = 0
        if u0 > 0:
            res_x0 = int(x0 + u0 * (x1 - x0) + 0.5)
            res_y0 = int(y0 + u0 * (y1 - y0) + 0.5)
        if u1 < 1:
            res_x1 = int(x0 + u1 * (x1 - x0) + 0.5)
            res_y1 = int(y0 + u1 * (y1 - y0) + 0.5)
        result = [[res_x0, res_y0], [res_x1, res_y1]]



    return result
