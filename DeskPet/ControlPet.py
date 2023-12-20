from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu, QSystemTrayIcon, QGraphicsPixmapItem, QGraphicsItem, QPushButton, QAbstractButton \
, QVBoxLayout, QFrame, QMessageBox

from PyQt6.QtGui import QIcon, QPixmap, QMovie, QAction, QImage, QTransform, QCursor, QPainter, QCloseEvent
from PyQt6.QtCore import  Qt, QTimer, QObject, QPoint, QUrl, QEvent, QRectF, QRect, QSize, QPropertyAnimation
import sys
import math
import pyautogui
import random

## Control Desk Pet actions
class PetControl(QWidget):
    def __init__(self):
        super(PetControl,self).__init__()
        self.basicbody = QLabel(self)
        
        
        #window configuration
        self.screen = pyautogui.size()
        # desktop = QApplication.desktop()
        # screen_rect = desktop.screenGeometry()
        # width, height = screen_rect.width(), screen_rect.height()

        # window_width, window_height = 200, 200
        # x = (width - window_width) // 2
        # y = (height - window_height) // 2

        

        # window.setGeometry(x, y, window_width, window_height)

        #boundary
        self.x_max = self.screen[0] - 48
        self.y_max = self.screen[1] - 200
        self.bound = []
        self.left = 400
        self.top = 400
        self.width = 350
        self.height = 350
        # set geometry of QWidget and remove border
        self.setGeometry(self.left,self.top,self.width,self.height)
        #self.setContentsMargins(0,0,0,0)
        self.mouse_drag_pos = None
        self.is_follow_mouse = False
        self.mouse_moving = False
        #self.btn1 = QPushButton(self)
        self.switch = QPushButton(self)
        self.switch.resize(24,24)
        self.switch.setStyleSheet("""
        background-color: white
        """)
        img = QImage()
        img.load("img/Switch1.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(24,25))
        self.switch.move(188,227)
        self.switch.setHidden(True)
        self.switch.pressed.connect(self.switch_press)
        self.switch.released.connect(self.switch_release)
        # self.addwidget(self.switch)
        # self.icon = QImage()
        # self.icon.load("img/Switch1.png")
        # self.switch_icon = QPixmap("img/Switch1.png")
        # self.switch.setIcon(self.switch_icon)
        # self.switch.setIconSize(QSize(200,200))
        #self.btn.setCheckable(True)
        # self.btn.clicked.connect(self.mousePressEvent)
        #Actions config
        self.appear = None
        self.idle = None
        self.thinking = None
        # self.idle_to_sleeping = None
        # self.sleeping = None
        # self.sleeping_to_idle = None
        # self.confusing = None
        # self.talking = None
        #initialize pet state
        self.event_number = 1
        self.state = 0

        self.i_frame = 0
        self.frame = QFrame(self)

        #New window
        self.menu = None

        self.get_actions()
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
        
        #transparent_img1.load()
        # load and resize images
        self.basicbody.setPixmap(QPixmap("img/body.png").scaled(200,200,Qt.AspectRatioMode.KeepAspectRatio))
        #self.switch.setStyleSheet("img/Switch1.png")
        #self.switch.clicked.connect(self.clickme)
        # self.body.move(500,500) # (100,100) as oringin
        # self.eyes.move(542,528)
        # self.ear1.move(420,420)
        # self.ear2.move(620,420)
        # self.foot1.move(455,625)
        # self.foot2.move(620,625)
        #take （400，400） as oringin
        print(self.pos().x(),self.pos().y())
        self.basicbody.move(100,100) #(100,100)
        
        #base = QPixmap.fromImage(transparent_img1).scaled(150,150,Qt.AspectRatioMode.KeepAspectRatio)
        print(self.basicbody.width()//2)
        self.show()
        QTimer.singleShot(1,self.update)

    def switch_press(self):
       self.switch.setStyleSheet("""
        background-color: white
        """)
       img = QImage()
       img.load(f"img/Switch2.png")
       pixmap = QPixmap(img)
       SwitchIcon = QIcon(pixmap)
       self.switch.setIcon(SwitchIcon)
       self.switch.setIconSize(QSize(23,23))

    def switch_release(self):
        self.switch.setStyleSheet("""
        background-color: white
        """)
        img = QImage()
        img.load(f"img/Switch1.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(24,25))
        self.menu = MenuButton(QCursor.pos().x(), QCursor.pos().y(),self)
        self.menu.quit.clicked.connect(self.menu.close)

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
        
 
        

    def load_png(self, images):
        pic_arr = []
        for image in images:
            img = QImage()
            print('img/' + image)
            img.load('img/' + image)
            pic_arr.append(img)
        return pic_arr
    
    def get_actions(self):
        self.idle = self.load_png(["idle1.png","idle2.png","idle2.png","idle2.png","open_eye3.png","idle1.png","open_eye3.png","idle1.png"])
        self.appear = self.load_png(["body.png","open_eye1.png","open_eye2.png",
                                     "open_eye1.png","open_eye2.png","ear_shaking2.png","ear_shaking1.png","ear_shaking3.png","idle1.png",
                                     "ear_shaking4.png","ear_shaking3.png","ear_shaking5.png","idle1.png"])

    def set_state(self):
        if self.event_number == 1:
            self.state = 0
            QTimer.singleShot(100,self.update)
            
        else:
            self.state = 1
            self.switch.setHidden(False)
            QTimer.singleShot(400,self.update)

    def update(self):
        #print(self.state)
        if self.state == 0:
            self.frame = self.appear[self.i_frame]
            self.animate(self.appear,2,4)
        elif self.state == 1:
            self.frame = self.idle[self.i_frame]
            self.animate(self.idle,2,4)

        self.basicbody.setPixmap(QPixmap.fromImage(self.frame).scaled(200,200,Qt.AspectRatioMode.KeepAspectRatio))
        QTimer.singleShot(100,self.set_state)

    def animate(self,array,a,b):
        if self.i_frame < len(array) - 1:
            self.i_frame += 1
        else:
            self.i_frame = 0
            self.event_number = random.randint(a,b)


class MenuButton(QWidget):
    def __init__(self, x, y, parent):
        super(MenuButton,self).__init__()
        self.parent = parent
        if x <=1800:
            self.setGeometry(x+50, y-50,550,150)
        else:
            self.setGeometry(x-250, y-50,550,150)
        self.interface = QLabel(self)
        self.battery = QPushButton(self)
        self.battery.resize(50,50)
        self.battery.move(10,0)
        self.chat = QPushButton(self)
        self.chat.resize(50,50)
        self.chat.move(60,0)
        self.quit = QPushButton(self)
        self.quit.resize(50,50)
        self.quit.move(110,0)
        #self.quit.setText("Exit")
        

        self.init_ui()

    def init_ui(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute(0x78))
        self.setAutoFillBackground(True)
        
        self.chat.setStyleSheet("background-color: transparent")
        chat_img = QPixmap("img/Setup_notChose.png")
        chat_icon = QIcon(chat_img)
        self.chat.setIcon(chat_icon)
        self.chat.setIconSize(QSize(20,20))

        self.battery.setStyleSheet("background-color: transparent")
        battery_img = QPixmap("img/Battery_notChose.png")
        battery_icon = QIcon(battery_img)
        self.battery.setIcon(battery_icon)
        self.battery.setIconSize(QSize(20,20))

        self.quit.setStyleSheet("background-color: transparent")
        quit_img = QPixmap("img/Exit_notChose.png")
        quit_icon = QIcon(quit_img)
        self.quit.setIcon(quit_icon)
        self.quit.setIconSize(QSize(20,20))
        self.quit.clicked.connect(self.close)

        self.show()

    def close(self):
        self.hide()
        # reply = QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QMessageBox.Yes | 
        #     QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()
        


class BodyButton(QPushButton):
    def __init__(self):
        super(BodyButton,self).__init__()


    

        
        
         
         

    
    
        