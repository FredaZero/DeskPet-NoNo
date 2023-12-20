from PyQt6.QtWidgets import QApplication, QGraphicsProxyWidget, QGraphicsPixmapItem,QGraphicsItem,QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QEvent, QPointF, QPropertyAnimation, QVariantAnimation, QSize, QRectF, QTimer, QObject, QEasingCurve
from PyQt6.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QTransform, QIcon, QCursor
import Items

class EarMovement(QGraphicsItem):  #QGraphicsView
    def __init__(self):
        super().__init__()
        self.mouse_drag_pos = None
        self.is_follow_mouse = False
        self.mouse_moving = False
        self.x_max = 1700 #scene.sceneRect().width()
        self.y_max = 900 #scene.sceneRect().height()
        self.animation = None
        self.L_ear = Items.Ear1Item()
        self.create_object()

        

    def create_object(self):
        
        self.animation = QPropertyAnimation(self.L_ear, b"rotation")
        self.animation.setDuration(200)
        self.animation.setStartValue(-50)
        self.animation.setKeyValueAt(0.25,-30)
        self.animation.setKeyValueAt(0.25,-50)
        self.animation.setKeyValueAt(0.25,-70)
        self.animation.setEndValue(-50)
        self.animation.setLoopCount(3)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        # scene.addItem(self.L_ear._item1)
        # self.setScene(scene)
        
        

    #action 1
    def mousePressEvent(self,event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            # 左键绑定拖拽
            self.is_follow_mouse = True
            print('clicked')
            self.animation.start()
            
#OPENAI_API_KEY=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 