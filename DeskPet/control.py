from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu, QSystemTrayIcon, QGraphicsPixmapItem, QGraphicsItem, QPushButton
from PyQt6.QtGui import QIcon, QPixmap, QMovie, QAction, QImage, QTransform, QCursor, QPainter
from PyQt6.QtCore import  Qt, QTimer, QObject, QPoint, QUrl, QEvent, QRectF, QRect, QSize
import sys
import math
import pyautogui

class PetControl(QWidget):
    def __init__(self):
        super(PetControl,self).__init__()
        self.body = QLabel(self)
        self.ear1 = QLabel(self)
        self.eyes = QLabel(self)
        self.ear2 = QLabel(self)
        self.foot1 = QLabel(self)
        self.foot2 = QLabel(self)

       
        
        #window configuration
        self.screen = pyautogui.size()
        #boundary
        self.x_max = self.screen[0] - 48
        self.y_max = self.screen[1] - 200
        self.bound = []
        self.left = 0
        self.top = 0
        self.width = 350
        self.height = 350
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.mouse_drag_pos = None
        self.is_follow_mouse = False
        self.mouse_moving = False
        self.btn = QPushButton(self)
        #self.btn.setCheckable(True)
        # self.btn.clicked.connect(self.mousePressEvent)

        self.set_up_pet()
    def set_up_pet(self):
        # img = QImage()
        # img.load("img/basicBody.png")
        #set up transparent window for images
        #setup window attribute
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute(0x78))
        self.setAutoFillBackground(True)

        transparent_img1 = QImage()
        transparent_img2 = QImage()
        transparent_img3 = QImage()
        transparent_img4 = QImage()
        transparent_img1.load("img/BasicBody.png")
        transparent_img2.load("img/BasicEyes.png")
        transparent_img3.load("img/Ears.png")
        transparent_img4.load("img/Foot.png")
        # load and resize images
        self.body.setPixmap(QPixmap.fromImage(transparent_img1).scaled(150,150,Qt.AspectRatioMode.KeepAspectRatio)) 
        self.eyes.setPixmap(QPixmap.fromImage(transparent_img2).scaled(60,60,Qt.AspectRatioMode.KeepAspectRatio))
        self.ear1.setPixmap(QPixmap.fromImage(transparent_img3).scaled(50,120,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(-45)))
        self.ear2.setPixmap(QPixmap.fromImage(transparent_img3).scaled(50,120,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(45)))
        self.foot1.setPixmap(QPixmap.fromImage(transparent_img4).scaled(50,60,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(45)))
        self.foot2.setPixmap(QPixmap.fromImage(transparent_img4).scaled(50,60,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(-45)))
        # self.body.move(500,500) # (100,100) as oringin
        # self.eyes.move(542,528)
        # self.ear1.move(420,420)
        # self.ear2.move(620,420)
        # self.foot1.move(455,625)
        # self.foot2.move(620,625)
        #take （400，400） as oringin
        print(self.pos().x(),self.pos().y())
        self.body.move(self.pos().x()+100,self.pos().y() + 100) #(100,100)
        self.eyes.move(self.pos().x()+142,self.pos().y()+128)
        self.ear1.move(self.pos().x()+20,self.pos().y()+20)
        self.ear2.move(self.pos().x()+220,self.pos().y()+20)
        self.foot1.move(self.pos().x()+55,self.pos().y()+225)
        self.foot2.move(self.pos().x()+220,self.pos().y()+225)
        #base = QPixmap.fromImage(transparent_img1).scaled(150,150,Qt.AspectRatioMode.KeepAspectRatio)
        print(self.body.width()//2)
        self.show()

    #action 1
    def mousePressEvent(self,event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 左键绑定拖拽
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPosition().toPoint() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
    def mouseMoveEvent(self,event):
        if Qt.MouseButton.LeftButton and self.is_follow_mouse:
            print(event.globalPosition().toPoint())
            print(self.pos())
            self.move(event.globalPosition().toPoint() - self.mouse_drag_pos)
            event.accept()
            
                
                

    def mouseReleaseEvent(self,event):
        self.is_follow_mouse = False
        if event.globalPosition().toPoint().x() >= self.x_max: 
            delta_x = self.x_max - self.pos().x()
            self.move(1900-delta_x,event.globalPosition().toPoint().y() - self.mouse_drag_pos.y())
        elif event.globalPosition().toPoint().x() <=35:
            delta_x = 35 - self.pos().x()
            self.move(45-delta_x,event.globalPosition().toPoint().y() - self.mouse_drag_pos.y())
        elif event.globalPosition().toPoint().y() >= self.y_max:
            delta_y = self.y_max - self.pos().y()
            self.move(event.globalPosition().toPoint().x() - self.mouse_drag_pos.x(),949-delta_y)
        elif event.globalPosition().toPoint().y() <=20:
            delta_y = 20 - self.pos().y()
            self.move(event.globalPosition().toPoint().x() - self.mouse_drag_pos.x(),35-delta_y)
        self.unsetCursor() #setCursor(QCursor(Qt.ArrowCursor))

    

        
        
         
         
class Movement(QWidget):
    def __init__(self,parent=PetControl):
        super(Movement,self).__init__(parent)
        self.parent = parent
        #initialize pet actions
        self.parent.img = None
        self.parent.appear = None
        self.parent.idle = None
        self.parent.thinking = None
        # self.idle_to_sleeping = None
        # self.sleeping = None
        # self.sleeping_to_idle = None
        # self.confusing = None
        # self.talking = None
        self.get_actions()
    
    def load_png(self, images):
        pic_arr = []
        for image in images:
            img = QImage()
            img.load('img/' + image)
            pic_arr.append(img)
        return pic_arr
    
    def get_actions(self):
        self.idle = self.load_png(["idle1.png","idle2.png"])
        self.appear = self.load_png(["body.png","open_eye1.png","open_eye2.png","ear_shaking2","ear_shaking1","ear_shaking3"])
        
        
        


        

## ear rotation with mouse event
# class PullEars(QGraphicsPixmapItem):
#     def __init__(self, parent=None):
#         super(PullEars, self).__init__(parent)
 
#         self.setFlag(QGraphicsItem.ItemIsMovable, True)
#         self.setTransformOriginPoint(self.boundingRect().center())
 
#     def set_pixmap(self):
#         pixmap = QPixmap("perro.jpg")
#         self.setPixmap(pixmap)
#         self.pixmap_controller = PetControl(self)
#         self.pixmap_controller.set_pixmap_controller()
#         self.pixmap_controller.setPos(self.boundingRect().topLeft())
#         self.pixmap_controller.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
 
#     def rotate_item(self, position):
#         item_position = self.transformOriginPoint()
#         angle = math.atan2(item_position.y() - position.y(), item_position.x() - position.x()) / math.pi * 180 - 45
#         print(angle)
#         self.setRotation(angle)
#         self.setPos(position)