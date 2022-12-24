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
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x1==x0:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        elif y1==y0:
            for x in range(x0, x1 + 1):
                result.append((x, y0))
        else:
            xDis = x1 - x0  # x的增量
            yDis = y1 - y0  # y的增量
            if abs(xDis) > abs(yDis):
                maxstep = abs(xDis)
            else:
                maxstep = abs(yDis)
            xUnitstep = xDis / maxstep  # x每步骤增量
            yUnitstep = yDis / maxstep # y的每步增量
            x = x0
            y = y0
            for k in range(maxstep):
                x = x + xUnitstep
                y = y + yUnitstep
                result.append((int(x),int(y))) #取整操作

    elif algorithm == 'Bresenham':
        if x1 == x0:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
                return result
        elif y1 == y0:
            for x in range(x0, x1 + 1):
                result.append((x, y0))
                return result
        else:
            k=(y1-y0)/(x1-x0)
            if x0 > x1: #交换坐标，保证从左到右画线
                x0,y0,x1,y1=x1,y1,x0,y0

            if k>1: #斜率大于1
                dx=x1-x0
                dy=y1-y0
                p=2*dx-dy
                result.append((x0,y0))
                y=y0
                x=x0
                for y in range(y0+1,y1+1):
                    if p<0:
                        p+=2*dx
                        result.append((x,y))
                    else:
                        p+=2*dx-2*dy
                        x+=1
                        result.append((x,y))

            elif k>0 and k<=1: #斜率为正且小于1
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dy - dx
                result.append((x0, y0))
                y = y0
                x = x0
                for x in range(x0 + 1, x1 + 1):
                    if p < 0:
                        p += 2 * dy
                        result.append((x, y))
                    else:
                        p += 2 * dy - 2 * dx
                        y += 1
                        result.append((x, y))

            elif k<0 and k>=-1:
                y1=2*y0-y1  #作对称变换到斜率为正
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dy - dx
                result.append((x0, y0))
                y = y0
                x = x0
                for x in range(x0 + 1, x1 + 1):
                    if p < 0:
                        p += 2 * dy
                        result.append((x, 2*y0-y))
                        #print(x, y)
                    else:
                        p += 2 * dy - 2 * dx
                        y += 1
                        result.append((x, 2*y0-y)) #再次作对称变换恢复
                        #print(x, y)
            else:
                y1 = 2*y0-y1#作对称变换到斜率为正
                dx = x1 - x0
                dy = y1 - y0
                p = 2 * dx - dy
                result.append((x0, y0))
                y = y0
                x = x0
                for y in range(y0 + 1, y1 + 1):
                    if p < 0:
                        p += 2 * dx
                        result.append((x, 2*y0-y))#再次作对称变换恢复
                        #print(x,y)
                    else:
                        p += 2 * dx - 2 * dy
                        x += 1
                        result.append((x, 2*y0-y))
                        #print(x, y)


    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i-1], p_list[i]], algorithm) #待修改为algorithm
        result += line
    return result

def draw_free(p_list, algorithm):
    """自由绘制

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []

    for i in range(len(p_list)-2):
        line = draw_line([p_list[i], p_list[i+1]], algorithm)#待修改为algorithm
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result=[]

    x0, y0 = p_list[0] #椭圆左上角坐标
    x1, y1 = p_list[1] #椭圆右下角坐标
    if x1<x0:
        d=x0
        x0=x1
        x1=d
    if y1<y0:
        d=y0
        y0=y1
        y1=d
    # 获取参数
    a=(x1-x0)/2
    b=(y1-y0)/2
    # 框架只是一个点或者一个线，绘图
    if a==0 or b==0:
        result=draw_line(p_list,'DDA')
        return result
    #圆心
    xc=(x1+x0)/2
    yc=(y1+y0)/2
    # 从点(0,b)开始
    x = 0
    y = b
    d = 4 * b * b - 4 * a * a * b + a * a
    while a * a * (2 * y - 1) >= 2 * (b * b * (x + 1)):
        result.append((x+xc, y+yc))
        result.append((-x+xc, y+yc))
        result.append((x+xc, -y+yc))
        result.append((-x+xc, -y+yc))
        if d < 0:
            d = d + 4 * b * b * (2 * x + 3)
        else:
            d = d + 4 * b * b * (2 * x + 3) - 8 * a * a * (y - 1)
            y =y- 1
        x =x+ 1
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
            x =x- 1
        y =y+ 1
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result=[]
    if algorithm=='Bezier':
        BEZIER_SAMPLE_COUNT = 1000
        delta=1/BEZIER_SAMPLE_COUNT
        t=0
        while t<=1:
            t=t+delta
            list=p_list
            #只剩一个点即是曲线上的点
            while len(list)>1:
                tmp=[]
                for i in range(len(list)-1):
                    x1, y1 = list[i]
                    x2, y2 = list[i+1]
                    tmp.append((t*x1+(1-t)*x2, t*y1+(1-t)*y2))
                list=tmp
            result+=list
    else:
        pass
    return result



def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for p in p_list:
        p.x+=dx
        p.y+=dy
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
        a=p.x
        b=p.y
        r=r*math.pi/180 # 角度转弧度
        p.x=a*math.cos(-r)-b*math.sin(-r);
        p.y=a*math.sin(-r)+b*math.cos(-r);

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
        p.x=s*p.x+(1-s)*x
        p.y=s*p.y+(1-s)*y
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
    pass
