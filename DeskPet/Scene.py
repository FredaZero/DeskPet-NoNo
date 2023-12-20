from PyQt6.QtWidgets import QApplication, QGraphicsProxyWidget, QGraphicsPixmapItem,QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QLabel, QFrame
from PyQt6.QtCore import Qt, QEvent, QPointF, QPropertyAnimation, QVariantAnimation, QSize, QRectF, QTimer, QObject
from PyQt6.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QTransform, QIcon, QCursor
import pyautogui
import module
import Items, View
import random

class Movement(QGraphicsView):
    def __init__(self,scene):
        super(Movement,self).__init__(scene)
        self.mouse_drag_pos = None
        self.is_follow_mouse = False
        self.mouse_moving = False
        self.x_max = 1700 #scene.sceneRect().width()
        self.y_max = 900 #scene.sceneRect().height()
    def mousePressEvent(self,event):
        super().mousePressEvent(event)
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
            # self.viewport().update()
            # QTimer.singleShot(1, self.update)
            event.accept()
    def mouseReleaseEvent(self,event):
        super().mouseReleaseEvent(event)
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
    #action 1
    


class MainScene(QWidget):
    def __init__(self) -> None:
        super(MainScene,self).__init__()

         # Switch
        self.switch = QPushButton()
        
        self.animation = None
        # self.switch.move(188,227)
        # self.switch.setHidden(True)
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

        #self.get_actions()

        self.init_ui()
        #self.get_animation()

    def init_ui(self):
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute(0x78))
        self.setAutoFillBackground(True)

        rect = pyautogui.size()
        scene = QGraphicsScene()#Movement()
        self.screen = pyautogui.size()
        
        self.x_max = self.screen[0] - 48
        self.y_max = self.screen[1] - 200

        body = QPixmap("img/body02.png").scaled(300,300,Qt.AspectRatioMode.KeepAspectRatio)
        ## QLabel
        self.body = QLabel(self)
        self.body.setPixmap(QPixmap("img/body02.png").scaled(300,300,Qt.AspectRatioMode.KeepAspectRatio))
        #self.item.fill(Qt.GlobalColor.transparent)
        # self.body = QGraphicsPixmapItem(body)
        # self.body.setZValue(2)
        # transform = QTransform()
        # transform.translate(100,100)
        # self.body.setTransform(transform)
        
        #self.body.setOpacity(0.5)  # 设置透明度
        
    
        #self.ear1 = View.EarMovement(Items.Ear1Item())#Items.Ear1Item() #QGraphicsPixmapItem(self.item)
        self.label1 = QLabel(self)
        self.ear1 = Items.Ear1Item(self.label1)
        self.label1.setPixmap(self.ear1._pixmap)
        #self.ear1.setPos(60,-15)
        #self.ear1 = QGraphicsPixmapItem(self.item)
        # self.ear1.setZValue(1)
        transform = QTransform()
        transform.translate(-20, 5)
        # self.ear1.setTransform(transform)
        #print(self.ear1.pos())
        # second ear 
        self.item = QPixmap("img/Ears2.png").scaled(120,120,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(50))
        self.ear2 = Items.Ear2Item(self.label1)
        #self.ear2.setPos(10,-35)
        # self.ear2 = QGraphicsPixmapItem(self.item)
        # self.ear2.setZValue(2)
        # transform = QTransform()
        # transform.translate(200, 5)
        # self.ear2.setTransform(transform)
        #eyes
        self.eye_item = QPixmap("img/BasicEyes02.png").scaled(60,60,Qt.AspectRatioMode.KeepAspectRatio)
        self.eyes = QGraphicsPixmapItem(self.eye_item)
        print('type: ',type(self.eyes))
        self.eyes.setZValue(3)
        self.eyes.setOpacity(0.8)
        transform = QTransform()
        transform.translate(120, 125)
        self.eyes.setTransform(transform)
        #foot1
        self.item = QPixmap("img/Foot2.png").scaled(50,50,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(60))
        self.foot1 = QGraphicsPixmapItem(self.item)
        self.foot1.setZValue(1)
        transform = QTransform()
        transform.translate(0, 230)
        self.foot1.setTransform(transform)
        #foot2
        self.item = QPixmap("img/Foot2.png").scaled(50,50,Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(-60))
        self.foot2 = QGraphicsPixmapItem(self.item)
        self.foot2.setZValue(1)
        transform = QTransform()
        transform.translate(250, 230)
        self.foot2.setTransform(transform)

        #switch
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.switch)
        self.switch.resize(25,25)
        self.switch.setStyleSheet("""
        background-color: transparent
        """)
        img = QImage()
        img.load("img/Switch1.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(25,25))
        proxy.setPos(120,180)
        proxy.setZValue(3)
        

        
        # #scene.setSceneRect(QRectF(0, 0,rect[0],rect[1]))
        # screen_w = scene.sceneRect().width()
        # screen_h = scene.sceneRect().height()
        # #self.resize(500,500)
        # print('width: ',screen_w)
        # print('height: ',screen_h)
        # #scene.setBackgroundLayer()
        
        
        # # scene.addItem(self.body)
        # scene.addItem(self.ear1)#.L_ear._item1)
        # scene.addItem(self.ear2)
        # scene.addItem(self.eyes)
        # scene.addItem(self.foot1)
        # scene.addItem(self.foot2)

        # scene.addItem(proxy)

        # self.switch.pressed.connect(self.switch_press)
        # self.switch.released.connect(self.switch_release)

        # view = Movement(scene)#View.EarMovement(scene) 
        # view.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        # view.setRenderHint(QPainter.RenderHint.Antialiasing)
        # view.setStyleSheet("""
        # background-color:transparent;
        # border:0px
        # """)
        # #scene.addItem(view.item1)
        # # view.setDragMode(QGraphicsView.ScrollHandDrag)
        # #view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # scene.setBackgroundBrush(QBrush(Qt.GlobalColor.transparent))
        
        # layout = QVBoxLayout()
        # layout.addWidget(view)

        # self.setLayout(layout)

        self.show()

    def switch_press(self):
       self.switch.setStyleSheet("""
        background-color: transparent
        """)
       img = QImage()
       img.load(f"img/Switch2.png")
       pixmap = QPixmap(img)
       SwitchIcon = QIcon(pixmap)
       self.switch.setIcon(SwitchIcon)
       self.switch.setIconSize(QSize(25,25))

    def switch_release(self):
        self.switch.setStyleSheet("""
        background-color: transparent
        """)
        img = QImage()
        img.load(f"img/Switch1.png")
        pixmap = QPixmap(img)
        SwitchIcon = QIcon(pixmap)
        self.switch.setIcon(SwitchIcon)
        self.switch.setIconSize(QSize(25,25))
        self.menu = MenuButton(QCursor.pos().x(), QCursor.pos().y(),self)
        self.menu.quit.clicked.connect(self.menu.close)

    # def load_png(self, images):
    #     pic_arr = []
    #     for image in images:
    #         img = QImage()
    #         print('img/' + image)
    #         img.load('img/' + image)
    #         pic_arr.append(img)
    #     return pic_arr
    
    # def get_actions(self):
    #     self.idle = self.load_png(["idle1.png","idle2.png","idle2.png","idle2.png","open_eye3.png","idle1.png","open_eye3.png","idle1.png"])
    #     self.appear = self.load_png(["body.png","open_eye1.png","open_eye2.png",
    #                                  "open_eye1.png","open_eye2.png","ear_shaking2.png","ear_shaking1.png","ear_shaking3.png","idle1.png",
    #                                  "ear_shaking4.png","ear_shaking3.png","ear_shaking5.png","idle1.png"])

    # def set_state(self):
    #     if self.event_number == 1:
    #         self.state = 0
    #         QTimer.singleShot(100,self.update)
            
    #     else:
    #         self.state = 1
    #         self.switch.setHidden(False)
    #         QTimer.singleShot(400,self.update)

    # def update(self):
    #     #print(self.state)
    #     if self.state == 0:
    #         self.frame = self.appear[self.i_frame]
    #         self.animate(self.appear,2,4)
    #     elif self.state == 1:
    #         self.frame = self.idle[self.i_frame]
    #         self.animate(self.idle,2,4)

    #     self.basicbody.setPixmap(QPixmap.fromImage(self.frame).scaled(200,200,Qt.AspectRatioMode.KeepAspectRatio))
    #     QTimer.singleShot(100,self.set_state)

    # def animate(self,array,a,b):
    #     if self.i_frame < len(array) - 1:
    #         self.i_frame += 1
    #     else:
    #         self.i_frame = 0
    #         self.event_number = random.randint(a,b)
        # self.animation = QPropertyAnimation(self.eye_item, b"pixmap")
        # self.eye_open = QPixmap("img/BasicEyes02.png").scaled(60,60,Qt.AspectRatioMode.KeepAspectRatio)
        # self.eye_close =QPixmap("img/EyeClose.png").scaled(60,60,Qt.AspectRatioMode.KeepAspectRatio)
        # self.animation.setStartValue(self.eye_open)
        # self.animation.setEndValue(self.eye_closed)
        # self.animation.setDuration(300)
        # self.animation.start()
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
            # self.viewport().update()
            # QTimer.singleShot(1, self.update)
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

            
                


class MenuButton(QWidget):
    def __init__(self, x, y, parent):
        super(MenuButton,self).__init__()
        self.parent = parent
        if x <=1800:
            self.setGeometry(x+90, y-50,550,150)
        else:
            self.setGeometry(x-250, y-50,550,150)
        self.interface = QLabel(self)
        self.battery = QPushButton(self)
        self.battery.resize(50,50)
        self.battery.move(10,0)
        self.chat = QPushButton(self)
        self.chat.resize(50,50)
        self.ask = None
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
        self.chat.setIconSize(QSize(30,30))
        self.chat.clicked.connect(self.chatbox)

        self.battery.setStyleSheet("background-color: transparent")
        battery_img = QPixmap("img/Battery_notChose.png")
        battery_icon = QIcon(battery_img)
        self.battery.setIcon(battery_icon)
        self.battery.setIconSize(QSize(30,30))

        self.quit.setStyleSheet("background-color: transparent")
        quit_img = QPixmap("img/Exit_notChose.png")
        quit_icon = QIcon(quit_img)
        self.quit.setIcon(quit_icon)
        self.quit.setIconSize(QSize(30,30))
        self.quit.clicked.connect(self.close)

        self.show()

    def close(self):
        self.hide()
        if self.ask is not None:
            self.ask.hide()

    def chatbox(self):
        #pass
        self.ask = module.ClippyChat()
        if self.ask.isHidden():
            self.ask.show()