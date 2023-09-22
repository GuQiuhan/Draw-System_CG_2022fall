#!/usr/bin/env python
# -*- coding:utf-8 -*-
#import os
import sys
import os
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem, QLabel, QPushButton, QLineEdit, QDialog, QMessageBox, QComboBox, QFrame, QScrollBar,
    QSlider, QFormLayout, QVBoxLayout, QFileDialog, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPixmap, QPen, QPalette, QBrush
from PyQt5.QtCore import QRectF, pyqtSlot, Qt
from PyQt5 import QtCore

# 全局变量
isGuest = False # 是否是游客模式


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.indeedPaint=False #是否真的画了
        self.isNewPolygon=False #判断是否是新图元
        self.isNewCurve=False

        self.pen=QPen()

    def start_draw_line(self, algorithm, item_id,p):
        self.pen=p
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def start_draw_polygon(self, algorithm, item_id,p):
        self.pen = p
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.isNewPolygon=True

    def start_draw_ellipse( self, item_id,p):
        self.pen = p
        self.status = 'ellipse'
        self.temp_algorithm = "null"
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id,p):
        self.pen = p
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.isNewCurve = True


    def start_draw_free(self, algorithm, item_id,p):
        self.pen = p
        self.status = 'freePainting'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self):
        if self.selected_id=='':
            return
        self.temp_item= self.item_dict[self.selected_id]
        translate_window=Translate()
        if translate_window.exec()==QDialog.Accepted:
            dx = translate_window.get_dx()
            dy = translate_window.get_dy()
            p_list2 = alg.translate(self.temp_item.p_list, dx, dy)
            self.temp_item = MyItem(self.temp_item.id, self.temp_item.item_type, p_list2, self.temp_item.algorithm, self.temp_item.pen)
            self.item_dict[self.selected_id] = self.temp_item
            self.item_dict[self.selected_id].update()


    def start_rotate(self):
        self.temp_item = self.item_dict[self.selected_id]
        rotate_window = Rotate()
        if rotate_window.exec() == QDialog.Accepted:
            x = rotate_window.get_x()
            y = rotate_window.get_y()
            r = rotate_window.get_r()
            p_list2 = alg.rotate(self.temp_item.p_list, x, y, r)
            self.temp_item = MyItem(self.temp_item.id, self.temp_item.item_type, p_list2, self.temp_item.algorithm,
                                    self.temp_item.pen)
            self.item_dict[self.selected_id] = self.temp_item
            self.item_dict[self.selected_id].update()

    def start_scale(self):
        self.temp_item = self.item_dict[self.selected_id]
        scale_window = Scale()
        if scale_window.exec() == QDialog.Accepted:
            x = scale_window.get_x()
            y = scale_window.get_y()
            s = scale_window.get_s()
            p_list2 = alg.scale(self.temp_item.p_list, x, y, s)
            self.temp_item = MyItem(self.temp_item.id, self.temp_item.item_type, p_list2, self.temp_item.algorithm,
                                    self.temp_item.pen)
            self.item_dict[self.selected_id] = self.temp_item
            self.item_dict[self.selected_id].update()

    def start_clip(self,algorithm):
        self.temp_item = self.item_dict[self.selected_id]
        if self.temp_item.item_type is not 'line':
            QMessageBox.warning(self, "Warning", "Only LINE can be cliped!", QMessageBox.Ok)
            return
        clip_window = Clip()
        if clip_window.exec() == QDialog.Accepted:
            x_min = clip_window.get_x_min()
            y_min = clip_window.get_y_min()
            x_max = clip_window.get_x_max()
            y_max = clip_window.get_y_max()
            if self.temp_item.scene()!=None:
                self.scene().removeItem(self.temp_item)
            p_list2 = alg.clip(self.temp_item.p_list, x_min, y_min, x_max, y_max,algorithm)

            item_list_p = self.scene().items()
            for p in  item_list_p:
                if p.id==self.temp_item.id:
                    self.scene().removeItem(p)
                    break

            self.temp_item = MyItem(self.temp_item.id, self.temp_item.item_type, p_list2, self.temp_item.algorithm,
                                    self.temp_item.pen)
            self.item_dict[self.selected_id] = self.temp_item
            self.item_dict[self.selected_id].selected = True
            self.scene().addItem(self.temp_item)


    def clear_selection(self):
        if self.selected_id != '' and self.item_dict!= {} and self.item_dict[self.selected_id] != None:
            item_list_p = self.scene().items()
            for p in item_list_p:
                if p.id == self.selected_id:
                    self.scene().removeItem(p)
                    self.temp_item = MyItem(self.temp_item.id, self.temp_item.item_type, self.temp_item.p_list,
                                            self.temp_item.algorithm,
                                            self.temp_item.pen)
                    self.item_dict[self.selected_id] = self.temp_item
                    self.item_dict[self.selected_id].selected = False
                    self.scene().addItem(self.temp_item)
                    break


            # self.item_dict[self.selected_id].selected = False
            # self.item_dict[self.selected_id].update()
        self.selected_id = ''
       # self.updateScene([self.sceneRect()])



    def selection_changed(self, selected):

        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '' and self.item_dict!={}:
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected

        if self.item_dict!= {} and self.selected_id != '' and self.item_dict[self.selected_id] != None:
            self.item_dict[selected].selected = True
            self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])


    #重写函数
    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':  #表示鼠标是在画线
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,self.pen)
            self.scene().addItem(self.temp_item)
        elif self.status=='polygon': #表示鼠标是在画多边形
            if self.isNewPolygon:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm,self.pen)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y]) # 表示目前的坐标
        elif self.status=='freePainting': #表示鼠标是在自由画
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm,self.pen)
            self.scene().addItem(self.temp_item)
        elif self.status == 'ellipse':  #表示鼠标是在画椭圆
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]],  self.temp_algorithm,self.pen)
            self.scene().addItem(self.temp_item)
        elif self.status=='curve': #表示鼠标是在画多边形
            if self.isNewCurve:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm,self.pen)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y]) # 表示目前的坐标
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)
        self.indeedPaint=True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y] #表示直线的终点
        elif self.status=='freePainting' or self.status=='polygon':
            self.temp_item.p_list.append([x, y])# 表示目前的坐标

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line'  or self.status=='freePainting'or self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item  #将当前的编号和当前的图元加入画布
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon':
            if self.isNewPolygon:
                self.item_dict[self.temp_id] = self.temp_item  # 将当前的编号和当前的图元加入画布
                self.list_widget.addItem(self.temp_id)
                self.isNewPolygon=False #将新创建的多边形图元加入后，就不是新图元了
        elif self.status == 'curve':
            if self.isNewCurve:
                self.item_dict[self.temp_id] = self.temp_item  # 将当前的编号和当前的图元加入画布
                self.list_widget.addItem(self.temp_id)
                self.isNewCurve=False #将新创建的多边形图元加入后，就不是新图元了
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)

class Translate(QDialog):
    """
    平移窗口
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("平移图形")
        self.resize(400, 200)
        self.label1 = QLabel('水平方向平移量:', self)
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(-200, 200)
        self.spinbox1.setSingleStep(1)
        self.spinbox1.setValue(0)
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label1)
        self.hlayout1.addWidget(self.spinbox1)

        self.label2 = QLabel('垂直方向平移量:', self)
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setRange(-200, 200)
        self.spinbox2.setSingleStep(1)
        self.spinbox2.setValue(0)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2)
        self.hlayout2.addWidget(self.spinbox2)

        self.button1 = QPushButton("Cancel", self)
        self.button1.clicked.connect(self.cancel)
        self.button2 = QPushButton("Translate", self)
        self.button2.setFocus()
        self.button2.clicked.connect(self.translate)
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.button1)
        self.hlayout3.addWidget(self.button2)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)

        self.setLayout(self.vlayout)



    @pyqtSlot()
    def translate(self):  # 查错并确认保存
        self.accept()

    def cancel(self):  # 取消保存
        self.reject()

    def get_dx(self):
        return self.spinbox1.value()

    def get_dy(self):
        return self.spinbox2.value()

class Rotate(QDialog):
    """
    旋转窗口
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("旋转图形")
        self.resize(400, 200)
        self.label1 = QLabel('旋转中心x坐标:', self)
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(0, 600)
        self.spinbox1.setSingleStep(1)
        self.spinbox1.setValue(0)
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label1)
        self.hlayout1.addWidget(self.spinbox1)

        self.label2 = QLabel('旋转中心y坐标:', self)
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setRange(0, 600)
        self.spinbox2.setSingleStep(1)
        self.spinbox2.setValue(0)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2)
        self.hlayout2.addWidget(self.spinbox2)

        self.label3 = QLabel('顺时针旋转角度:', self)
        self.spinbox3 = QSpinBox(self)
        self.spinbox3.setRange(0, 720)
        self.spinbox3.setSingleStep(1)
        self.spinbox3.setValue(0)
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.label3)
        self.hlayout3.addWidget(self.spinbox3)

        self.button1 = QPushButton("Cancel", self)
        self.button1.clicked.connect(self.cancel)
        self.button2 = QPushButton("Rotate", self)
        self.button2.clicked.connect(self.rotate)
        self.button2.setFocus()
        self.hlayout4 = QHBoxLayout()
        self.hlayout4.addWidget(self.button1)
        self.hlayout4.addWidget(self.button2)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)
        self.vlayout.addLayout(self.hlayout4)

        self.setLayout(self.vlayout)



    @pyqtSlot()
    def rotate(self):  # 查错并确认保存
        self.accept()

    def cancel(self):  # 取消保存
        self.reject()

    def get_x(self):
        return self.spinbox1.value()

    def get_y(self):
        return self.spinbox2.value()

    def get_r(self):
        return self.spinbox3.value()

class Scale(QDialog):
    """
    缩放窗口
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("缩放图形")
        self.resize(400, 200)
        self.label1 = QLabel('缩放中心x坐标:', self)
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(0, 600)
        self.spinbox1.setSingleStep(1)
        self.spinbox1.setValue(0)
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label1)
        self.hlayout1.addWidget(self.spinbox1)

        self.label2 = QLabel('缩放中心y坐标:', self)
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setRange(0, 600)
        self.spinbox2.setSingleStep(1)
        self.spinbox2.setValue(0)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2)
        self.hlayout2.addWidget(self.spinbox2)

        self.label3 = QLabel('缩放倍数:', self)
        self.spinbox3 = QDoubleSpinBox(self)
        self.spinbox3.setRange(0, 10)
        self.spinbox3.setSingleStep(0.1)
        self.spinbox3.setValue(0)
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.label3)
        self.hlayout3.addWidget(self.spinbox3)

        self.button1 = QPushButton("Cancel", self)
        self.button1.clicked.connect(self.cancel)
        self.button2 = QPushButton("Scale", self)
        self.button2.clicked.connect(self.scale)
        self.button2.setFocus()
        self.hlayout4 = QHBoxLayout()
        self.hlayout4.addWidget(self.button1)
        self.hlayout4.addWidget(self.button2)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)
        self.vlayout.addLayout(self.hlayout4)

        self.setLayout(self.vlayout)



    @pyqtSlot()
    def scale(self):  # 查错并确认保存
        self.accept()

    def cancel(self):  # 取消保存
        self.reject()

    def get_x(self):
        return self.spinbox1.value()

    def get_y(self):
        return self.spinbox2.value()

    def get_s(self):
        return self.spinbox3.value()

class Clip(QDialog):
    """
    缩放窗口
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("裁剪图形")
        self.resize(400, 200)
        self.label1 = QLabel('裁剪窗口左上角x坐标:', self)
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setRange(0, 600)
        self.spinbox1.setSingleStep(1)
        self.spinbox1.setValue(0)
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label1)
        self.hlayout1.addWidget(self.spinbox1)

        self.label2 = QLabel('裁剪窗口左上角y坐标:', self)
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setRange(0, 600)
        self.spinbox2.setSingleStep(1)
        self.spinbox2.setValue(0)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2)
        self.hlayout2.addWidget(self.spinbox2)

        self.label3 = QLabel('裁剪窗口右下角x坐标:', self)
        self.spinbox3 = QSpinBox(self)
        self.spinbox3.setRange(0, 600)
        self.spinbox3.setSingleStep(1)
        self.spinbox3.setValue(0)
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.label3)
        self.hlayout3.addWidget(self.spinbox3)

        self.label4 = QLabel('裁剪窗口右下角y坐标:', self)
        self.spinbox4 = QSpinBox(self)
        self.spinbox4.setRange(0, 600)
        self.spinbox4.setSingleStep(1)
        self.spinbox4.setValue(0)
        self.hlayout4 = QHBoxLayout()
        self.hlayout4.addWidget(self.label4)
        self.hlayout4.addWidget(self.spinbox4)

        self.button1 = QPushButton("Cancel", self)
        self.button1.clicked.connect(self.cancel)
        self.button2 = QPushButton("Clip", self)
        self.button2.clicked.connect(self.clip)
        self.button2.setFocus()
        self.hlayout5 = QHBoxLayout()
        self.hlayout5.addWidget(self.button1)
        self.hlayout5.addWidget(self.button2)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)
        self.vlayout.addLayout(self.hlayout4)
        self.vlayout.addLayout(self.hlayout5)

        self.setLayout(self.vlayout)



    @pyqtSlot()
    def clip(self):  # 查错并确认保存
        self.accept()

    def cancel(self):  # 取消保存
        self.reject()

    def get_x_min(self):
        return self.spinbox1.value()

    def get_y_min(self):
        return self.spinbox2.value()

    def get_x_max(self):
        return self.spinbox3.value()

    def get_y_max(self):
        return self.spinbox4.value()

class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', pen: QPen=None ,parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.pen=pen



    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.pen) #首先设置画笔
        if self.item_type == 'line':
            print(self.p_list)
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p) # 使用QPainter来将具体像素数值转化到图上
            if self.selected:
                painter.setPen(QColor(255, 0, 0))  #选中图元框红框
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))  # 选中图元框红框
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'freePainting':
            item_pixels = alg.draw_free(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))  # 选中图元框红框
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))  # 选中图元框红框
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            # 画控制多边形
            if len(self.p_list)!=1 :
                result = []
                for i in range(len(self.p_list)-1):
                    line = alg.draw_line([self.p_list[i], self.p_list[i+1]], 'DDA')  # 待修改为algorithm
                    result += line
                for p in result:
                    painter.setPen(QPen(QColor(128, 128, 0), 2))
                    painter.drawPoint(*p)
            # 画控制点
            for p in self.p_list:
                painter.setPen(QPen(QColor(255, 255, 0), 5))
                painter.drawPoint(*p)
            # 画曲线
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.pen)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))  # 选中图元框红框
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            if self.p_list==[]:
                return QRectF(0,0,0,0)
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon' or self.item_type=='freePainting'or self.item_type=='curve'or self.item_type == 'ellipse':
            x0,y0=self.p_list[0] #最小值
            x1,y1=x0,y0 #最大值
            for x,y in self.p_list:
                if x<x0: x0=x
                if y<y0: y0=y
                if x>x1: x1=x
                if y>y1: y1=y
            w = x1-x0
            h = y1-y0
            return QRectF(x0-1, y0 - 1, w + 2, h + 2)

    # def mousePressEvent(self,event: QMouseEvent):
    #     print("here")
    #     self.setFocus()
    #     self.selected=True
    #     self.update()

    def get_id(self):
        _id = self.id
        #self.item_cnt += 1
        return _id

class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)

        #self.setStyleSheet("background-image: url(QTImages/bkg.jpg);")

        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        save_canvas_act = file_menu.addAction('保存画布')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        freePainting_act = draw_menu.addAction('自由笔画')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        #设置右侧下拉框
        # self.shapeLabel = QLabel("形状： ")  # label的初始化
        # self.shapeComboBox = QComboBox()  # ComboBox的初始化
        # self.shapeComboBox.addItem("线段", 0)  # ComboBox添加项目
        # self.shapeComboBox.addItem("多边形", 1)
        # self.shapeComboBox.addItem("椭圆", 2)
        # self.shapeComboBox.addItem("曲线", 3)
        # self.shapeComboBox.addItem("自由笔画", 4)
        # self.shapeComboBox.activated[int].connect(self.setShape)  # 绑定槽函数self.showShape()。当下拉选项被激发，则发送类型为int型的信号。

        #设置画笔选项
        self.colorlabel = QLabel('画笔颜色：')
        self.Rlabel = QLabel('R：')
        self.scrollbarr = QSlider(Qt.Horizontal)
        self.scrollbarr.setMaximum(255)
        self.Glabel = QLabel('G：')
        self.scrollbarg = QSlider(Qt.Horizontal)
        self.scrollbarg.setMaximum(255)
        self.Blabel = QLabel('B：')
        self.scrollbarb = QSlider(Qt.Horizontal)
        self.scrollbarb.setMaximum(255)
        self.Tlabel = QLabel('透明度：')
        self.scrollbart = QSlider(Qt.Horizontal)
        self.scrollbart.setMaximum(255)
        self.scrollbart.setValue(255)
        self.widthlabel = QLabel('画笔粗细：')
        self.scrollbarwidth = QSlider(Qt.Horizontal)
        self.scrollbarwidth.setRange(1, 20)
        self.scrollbarwidth.setValue(4)
        self.scrollbarwidth.setTickPosition(QSlider.TicksAbove)
        # self.penshapeLabel = QLabel("画笔格式：")  # label的初始化
        # self.penshapeComboBox = QComboBox()  # ComboBox的初始化
        # self.penshapeComboBox.addItem("实线", 0)  # ComboBox添加项目
        # self.penshapeComboBox.addItem("短线", 1)
        # self.penshapeComboBox.addItem("点线", 2)
        # self.penshapeComboBox.addItem("点横线1", 3)
        # self.penshapeComboBox.addItem("点横线2", 4)

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        freePainting_act.triggered.connect(self.freePainting_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)

        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
       # self.list_widget.currentTextChanged.connect(self.SelectionChanged)

        # 设置主窗口的布局
        # 添加表单布局
        self.gridlayout1 = QFormLayout()
        self.gridlayout1.addRow(self.colorlabel)
        self.gridlayout1.addRow(self.Rlabel, self.scrollbarr)
        self.gridlayout1.addRow(self.Glabel, self.scrollbarg)
        self.gridlayout1.addRow(self.Blabel, self.scrollbarb)
        self.gridlayout1.addRow(self.Tlabel, self.scrollbart)
        self.gridlayout1.addRow(self.widthlabel,self.scrollbarwidth)
        #self.gridlayout1.addRow(self.penshapeLabel,self.penshapeComboBox)
        # 添加笔刷之类的垂直布局
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.gridlayout1)
        self.vbox.addWidget(self.list_widget, stretch=1)
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addLayout(self.vbox)
        self.hbox_layout.setStretchFactor(self.canvas_widget, 3)
        self.hbox_layout.setStretchFactor(self.vbox, 1)
        #self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def SelectionChanged(self):
        if self.list_widget.currentRow()==-1:
            return
        self.canvas_widget.selection_changed()

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def add_id(self):
        self.item_cnt+=1

    def setPen(self,pen):
        pen.setColor(QColor(self.scrollbarr.value(),self.scrollbarg.value(),self.scrollbarb.value(),self.scrollbart.value()))
        pen.setWidth(self.scrollbarwidth.value())
        # value=self.penshapeComboBox.currentIndex()
        # print(value)
        # if value==0:
        #     pen.setStyle(Qt.SolidLine)
        # elif value==1:
        #     pen.setStyle(Qt.DashLine)
        # elif value==2:
        #     pen.setStyle(Qt.DotLine)
        # elif value==3:
        #     pen.setStyle(Qt.DashDotLine)
        # elif value==4:
        #     pen.setStyle(Qt.DashDotDotLine)


    def line_naive_action(self):
        pen=QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_line('Naive', self.get_id(),pen)
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_line('DDA', self.get_id(),pen)
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_line('Bresenham', self.get_id(),pen)  #待写
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_polygon('DDA', self.get_id(),pen)
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id(),pen)
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_ellipse(self.get_id(),pen)  # 待写
        self.statusBar().showMessage('中点圆算法绘制椭圆')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_curve('Bezier',self.get_id(),pen)  # 待写
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_curve('B-spline',self.get_id(),pen)
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def freePainting_action(self):
        pen = QPen()
        self.setPen(pen)
        self.canvas_widget.start_draw_free('DDA', self.get_id(),pen)
        self.statusBar().showMessage('自由笔画')
        self.list_widget.clearSelection()
        #self.list_widget.setCurrentRow(-1)
        self.canvas_widget.clear_selection()

    def translate_action(self):
        if self.list_widget.currentRow()==-1:
            QMessageBox.warning(self, "Warning", "No item selected!", QMessageBox.Ok)
            return
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移变换')
        # self.list_widget.clearSelection()
        # self.list_widget.setCurrentRow(-1)
        # self.canvas_widget.clear_selection()

    def rotate_action(self):
        if self.list_widget.currentRow()==-1:
            QMessageBox.warning(self, "Warning", "No item selected!", QMessageBox.Ok)
            return
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转变换')
        # self.list_widget.clearSelection()
        # self.canvas_widget.clear_selection()

    def scale_action(self):
        if self.list_widget.currentRow()==-1:
            QMessageBox.warning(self, "Warning", "No item selected!", QMessageBox.Ok)
            return
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放变换')
        # self.list_widget.clearSelection()
        # self.canvas_widget.clear_selection()

    def clip_cohen_sutherland_action(self):
        if self.list_widget.currentRow()==-1:
            QMessageBox.warning(self, "Warning", "No item selected!", QMessageBox.Ok)
            return
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法裁剪线段')
        # self.list_widget.clearSelection()
        # self.canvas_widget.clear_selection()

    def clip_liang_barsky_action(self):
        if self.list_widget.currentRow()==-1:
            QMessageBox.warning(self, "Warning", "No item selected!", QMessageBox.Ok)
            return
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('Liang-Barsky算法裁剪线段')
        # self.list_widget.clearSelection()
        # self.canvas_widget.clear_selection()

    def reset_canvas_action(self):
        self.canvas_widget.clear_selection()
        self.canvas_widget.item_dict={}
        self.item_cnt = 0

        n=self.list_widget.count()
        for i in range(n - 1, -1, -1):
            self.list_widget.removeItemWidget(self.list_widget.takeItem(i))

        self.scene.clear()

    def save_canvas_action(self):
        pix = self.canvas_widget.grab()
        save_window=SavePix(pix)
        if save_window.exec()==QDialog.Accepted:
            save_window.close()
            pix_window = Pix(pix)
            pix_window.exec()





class SavePix(QDialog):
    """
    填写保存路径窗口
    """

    def __init__(self,pixmap):
        super().__init__()

        self.setWindowTitle("保存画布")
        self.resize(400, 200)
        self.pix=pixmap
        self.label1 = QLabel('保存至:', self)
        self.line1 = QLineEdit(self)
        self.button = QPushButton('···')
        self.button.clicked.connect(self.showDir)
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label1)
        self.hlayout1.addWidget(self.line1)
        self.hlayout1.addWidget(self.button)

        self.label2 = QLabel('命名为:', self)
        self.line2 = QLineEdit(self)
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label2)
        self.hlayout2.addWidget(self.line2)

        self.button1 = QPushButton("Cancel", self)
        self.button1.clicked.connect(self.cancel)
        self.button2 = QPushButton("Save", self)
        self.button2.setFocus()
        self.button2.clicked.connect(self.save)
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.button1)
        self.hlayout3.addWidget(self.button2)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)

        self.setLayout(self.vlayout)



    @pyqtSlot()
    def save(self):  # 查错并确认保存
        if self.line1.text()!= "" :
            if os.path.exists(self.line1.text()): # 目录合法
                name=self.line1.text()+"/"+self.line2.text()+".jpg"
                self.pix.save(name)
                self.accept()

            else:
                QMessageBox.warning(self, "Warning", "Path Error!", QMessageBox.Ok)
                self.line1.clear()  # 清空，用于下一次注册
                self.line1.setFocus()


        else:
            QMessageBox.warning(self, "Warning","Path can not be empty!", QMessageBox.Ok)
            self.line1.clear()  # 清空，用于下一次注册
            self.line1.setFocus()


    def cancel(self):  # 取消保存
        self.reject()

    def showDir(self):
        m = QFileDialog.getExistingDirectory(None, "Select the directory:")  # 起始路径
        self.line1.setText(m)

class Pix(QDialog):
    """
    展示保存图片窗口
    """
    def __init__(self,pixmap):
        super().__init__()
        self.setWindowTitle("图片展示(保存成功！)")
        self.layout = QHBoxLayout()
        self.label = QLabel()
        self.label.resize(800, 480)
        self.pix = pixmap.scaled(self.label.width(), self.label.height())
        self.label.setPixmap(self.pix)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class Login(QDialog):
    """
    登陆窗口类，包括用户注册功能
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(613, 306)

        self.label1 = QLabel('Username:',self)
        self.label1.setGeometry(27, 60,71 , 20)
        self.line1 = QLineEdit(self)
        self.line1.setGeometry(110, 60, 181, 21)
        self.label2 = QLabel('Password:',self)
        self.label2.setGeometry(27, 100,71 , 20)
        self.line2 = QLineEdit(self)
        self.line2.setGeometry(110, 100, 181, 21)

        self.button1=QPushButton("Log in User",self)
        self.button1.setGeometry(140,140,121,32)
        self.button1.clicked.connect(self.on_click1)
        self.button2=QPushButton("Register",self)
        self.button2.setGeometry(140,180,121,32)
        self.button2.clicked.connect(self.on_click2)
        self.button3=QPushButton("Guest Visit",self)
        self.button3.setGeometry(140,220,121,32)
        self.button3.clicked.connect(self.on_click3)
        self.button4=QPushButton("Exit",self)
        self.button4.setGeometry(140,260,121,32)
        self.button4.clicked.connect(self.on_click4)

        pic = QLabel(self)
        pixmap = QPixmap("QTImages/login_pic.png") # 按指定路径找到图片
        pic.setScaledContents(True)  # 让图片自适应label大小
        pic.setPixmap(pixmap)  # 在label上显示图片
        pic.setGeometry(340, 15, 261, 271)


    def Check(self,name,pwd):
        return True


    @pyqtSlot()
    def on_click1(self):  # 登陆界面
        # 检查用户名合法性
        if self.Check(self.line1.text(), self.line2.text()):
            QMessageBox.information(self, "Title", "Login Success!")
            self.accept()
        else:
            QMessageBox.warning(self, "Warning","Username or password error!", QMessageBox.Ok)
            self.line1.clear()
            self.line2.clear()
            self.line1.setFocus()


    def on_click2(self):  # 注册界面
        r=Register()
        if r.exec()==QDialog.Accepted:
            r.close()

    def on_click3(self):  # 游客登陆界面
        global isGuest
        isGuest = True #修改全局变量为false
        self.accept()

    def on_click4(self):  # 退出界面
        self.close()

class Register(QDialog):
    """
    注册窗口类
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Register")
        self.resize(400, 300)

        self.label1 = QLabel('Username:', self)
        self.label1.setGeometry(20, 60, 81, 20)
        self.line1 = QLineEdit(self)
        self.line1.setGeometry(110, 60, 221, 21)
        self.label2 = QLabel('Password:', self)
        self.label2.setGeometry(20, 100, 81, 20)
        self.line2 = QLineEdit(self)
        self.line2.setGeometry(110, 100, 221, 21)
        self.label3 = QLabel('Password again', self)
        self.label3.setGeometry(20, 140, 81, 20)
        self.line3 = QLineEdit(self)
        self.line3.setGeometry(130, 140, 201, 21)

        self.button1 = QPushButton("Register", self)
        self.button1.setGeometry(40, 220, 112, 32)
        self.button1.clicked.connect(self.on_click1)
        self.button2 = QPushButton("Cancel", self)
        self.button2.setGeometry(230, 220, 112, 32)
        self.button2.clicked.connect(self.on_click2)

    @pyqtSlot()
    def on_click1(self):  # 查错并确认注册
        if self.line1.text()!= "" and self.line2.text() == self.line3.text():
            #检查是否重名
            if 1:
                QMessageBox.information(self, "Title", "Register Success!")
                self.accept()

            else:
                QMessageBox.warning(self, "Warning","Username has existed!", QMessageBox.Ok)
                self.line1.clear()  # 清空，用于下一次注册
                self.line2.clear()
                self.line3.clear()
                self.line1.setFocus()


        else:
            QMessageBox.warning(self, "Warning","Username or password error!", QMessageBox.Ok)
            self.line1.clear()  # 清空，用于下一次注册
            self.line2.clear()
            self.line3.clear()
            self.line1.setFocus()


    def on_click2(self):  # 取消注册
        self.reject()


class Login2(QDialog):
    """
    简单登陆窗口类
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(487, 322)

        self.label1 = QLabel(self)
        self.label1.setGeometry(30, 30, 1200 , 100)
        pix = QPixmap("QTImages/login2.png")
        self.label1.setPixmap(pix)
        self.label1.setScaledContents(True)  # 自适应QLabel大小

        self.button1=QPushButton("Start Now",self)
        self.button1.setGeometry(180,270,112,32)
        self.button1.clicked.connect(self.on_click1)

        palette = QPalette()
        pix = QPixmap("QTImages/bkg.jpg")

        pix = pix.scaled(self.width(),self.height())

        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        # self.painter=QPainter(self)
        # self.painter.drawPixmap(self.rect(), QPixmap("QTImage/bkg.jpg"), self.rect())


    @pyqtSlot()
    def on_click1(self):  # 登陆界面
        self.accept()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    l=Login2()
    if l.exec()==QDialog.Accepted:
        mw = MainWindow()
        mw.show()
    sys.exit(app.exec_())
