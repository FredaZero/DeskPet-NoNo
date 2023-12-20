from PyQt6.QtWidgets import QApplication, QGraphicsProxyWidget, QGraphicsPixmapItem,QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QEvent, QPointF, QPropertyAnimation, QVariantAnimation, QSize
from PyQt6.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QTransform, QIcon, QCursor

class ClickBody(QGraphicsPixmapItem):
    def __init__(self):
        super(ClickBody,self).__init__()