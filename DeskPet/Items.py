import sys
from PyQt6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
QGraphicsPixmapItem, QGraphicsObject)
from PyQt6.QtCore import (Qt, QObject, QPointF, QRectF,
QPropertyAnimation, pyqtProperty, pyqtSignal, QByteArray, QEasingCurve)
from PyQt6.QtGui import QPixmap, QTransform
import Items

class Ear1Item(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._rotation = -50
        self._pixmap = QPixmap(f"img/Ears2.png").scaled(120,120,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self._rotation))
        # self.setTransformOriginPoint(self._pixmap.width(),self._pixmap.height()) 
        # self._item1 = QGraphicsPixmapItem(self._pixmap)
        # #self._item1.setZValue(1)
        # # transform = QTransform()
        # # transform.translate(-10, 20)
        # # self._item1.setTransform(transform)
        
        # print(self._item1.pos())
        # self._item1.setTransformOriginPoint(self._item1.boundingRect().bottomLeft())
        # self._item1.setPos(QPointF(60,-15))
        # self._item1.setRotation(self._rotation)
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(200)
        
        
    #     self.animation = QPropertyAnimation(self, b"rotation")
    #     self.animation.setDuration(1000)
    #     self.animation.setStartValue(-20)
    #     self.animation.setEndValue(-70)
    #     self.animation.setLoopCount(3)
    #     self.animation.setEasingCurve(QEasingCurve.InOutSine)

    # def mousePressEvent(self,event):
    #     self.animation.start()
    @pyqtProperty(int)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self,value):
        self._rotation = value
        transform = QTransform()
        transform.rotate(self._rotation)
        self._rotated_pixmap = self._pixmap.transformed(transform)
        self.update()

    def boundingRect(self):
        return QRectF(-72, -0.2*self._pixmap.height(),
                      3.2*self._pixmap.width(), 1.3*self._pixmap.height())

    def paint(self, painter, option, widget):
        painter.save()  # 保存当前的坐标系统状态

        # 将原点移动到 QPixmap 的左下角
        painter.translate(12, self._pixmap.height())
        painter.rotate(self._rotation)
        # 反转 y 轴
        #painter.scale(0, -1)

        # 绘制 QPixmap
        painter.drawPixmap(0,-self._pixmap.height(), self._pixmap)

        painter.restore()  # 恢复到保存的坐标系统状态
    
        #self.L_ear = Items.Ear1Item()
        

    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            # 左键绑定拖拽
            self.is_follow_mouse = True
            print('clicked')
            self.animation.setStartValue(-50)
            self.animation.setKeyValueAt(0.25,-30)
            self.animation.setKeyValueAt(0.25,-50)
            self.animation.setKeyValueAt(0.25,-70)
            self.animation.setEndValue(-50)
            self.animation.setLoopCount(3)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            self.animation.start()
            event.accept()


class Ear2Item(QObject):
    def __init__(self,parent=None):
        super().__init__(parent)
        self._rotation = 50
        self._pixmap = QPixmap(f"img/Ears2.png").scaled(120,120,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self._rotation))
        # self.setTransformOriginPoint(self._pixmap.width(),self._pixmap.height()) 
        # self._item1 = QGraphicsPixmapItem(self._pixmap)
        # #self._item1.setZValue(1)
        # # transform = QTransform()
        # # transform.translate(-10, 20)
        # # self._item1.setTransform(transform)
        
        # print(self._item1.pos())
        # self._item1.setTransformOriginPoint(self._item1.boundingRect().bottomLeft())
        # self._item1.setPos(QPointF(60,-15))
        # self._item1.setRotation(self._rotation)
        self.animation = QPropertyAnimation(self, b"rotation")
        self.animation.setDuration(200)
        
        
    #     self.animation = QPropertyAnimation(self, b"rotation")
    #     self.animation.setDuration(1000)
    #     self.animation.setStartValue(-20)
    #     self.animation.setEndValue(-70)
    #     self.animation.setLoopCount(3)
    #     self.animation.setEasingCurve(QEasingCurve.InOutSine)

    # def mousePressEvent(self,event):
    #     self.animation.start()
    @pyqtProperty(int)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self,value):
        self._rotation = value
        transform = QTransform()
        transform.rotate(self._rotation)
        self._rotated_pixmap = self._pixmap.transformed(transform)
        self.update()

    def boundingRect(self):
        return QRectF(200, -0.2*self._pixmap.height(),
                      6.5*self._pixmap.width(), 1.4*self._pixmap.height())

    def paint(self, painter, option, widget):
        painter.save()  # 保存当前的坐标系统状态

        # 将原点移动到 QPixmap 的左下角
        painter.translate(200, self._pixmap.height())
        painter.rotate(self._rotation)
        
        # 反转 y 轴
        #painter.scale(0, -1)

        # 绘制 QPixmap
        painter.drawPixmap(0,-self._pixmap.height(), self._pixmap)

        painter.restore()  # 恢复到保存的坐标系统状态
    
        #self.L_ear = Items.Ear1Item()
        

    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            # 左键绑定拖拽
            self.is_follow_mouse = True
            print('clicked')
            self.animation.setStartValue(50)
            self.animation.setKeyValueAt(0.25,30)
            self.animation.setKeyValueAt(0.25,50)
            self.animation.setKeyValueAt(0.25,70)
            self.animation.setEndValue(50)
            self.animation.setLoopCount(3)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            self.animation.start()
            event.accept()