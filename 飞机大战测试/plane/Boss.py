# -*- coding:utf-8 -*-
import pygame
import os
import time
import random
from pygame.locals import *
import sys
import Mmain

WINDOW_WIDTH = 480  # 窗口宽
WINDOW_HEIGHT = 852 #窗口高
ENEMY_COUNT = 4     #敌机数量
enemy_list = []   #敌机的列表
plane_list = []
score = 0  #得分

class Item:
    #界面元素类
    window = None
    def __init__(self,img_path,x,y):
        self.img = pygame.image.load(img_path)#元素图片
        self.x = x  #元素坐标
        self.y = y
        #Item.window = window  #元素窗口

    def display(self):
        """贴图"""
        self.window.blit(self.img,(self.x,self.y))

class Map(Item):
    #地图类

    def map_move(self):
        if self.y >= -1124:
            self.y -= 1
        else:
            self.y = 0

class Bullet(Item):
    """子弹类"""
    def move(self):
        """向上移"""
        self.y -= 5
    def move_bullet(self):

        self.y += 5
    def __del__(self):
        print('对象删除')

    def is_hit_plane(self,enemy):
        """判断是否击中敌机"""
        bullet_rect = Rect(self.x,self.y,22,22)
        enemy_rect = Rect(enemy.x,enemy.y,60,30)
        return pygame.Rect.colliderect(bullet_rect,enemy_rect)

class BasePlane(Item):
    #飞机基类
    pass

class EnemyPlane(BasePlane):
    """敌人飞机类"""
    def __init__(self,img_path,x,y):
        super().__init__(img_path,x,y)
        self.is_hited = False #记录是否被击中
        self.bullets = []  # 记录子弹
        self.direction = "right"  # 用来存储飞机默认的显示方向


    def move(self):

        if self.direction == "right":
            self.x += 5

        elif self.direction == "left":
            self.x -= 5

        if self.x > 480 - 165:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"


    #敌机开火
    def fire(self):
        random_num = random.randint(1, 40)
        if random_num == 8:
            bullet = Bullet("../img/bomb-2.gif",self.x+82,self.y+250)
            bullet.display()
            #添加子弹
            self.bullets.append(bullet)

    def display_bullet(self):

        delete_bullets = []
        for bullet in self.bullets:
            if bullet.y >= 0:
                # 判断是否击中飞机
                for enemy in plane_list:
                    if bullet.is_hit_plane(enemy):  # 击中某架飞机
                        # 记录要删除的子弹
                        delete_bullets.append(bullet)
                        # 让敌机记录被击中的状态
                        enemy.is_hited = True
                        # global score
                        # score += 10
                        break
                    else:
                        bullet.display()
                        bullet.move_bullet()
            else:
                delete_bullets.append(bullet)

        for out_window_bullet in delete_bullets:
            self.bullets.remove(out_window_bullet)

class HeroPlane(BasePlane):
    """英雄飞机类"""
    def __init__(self,img_path,x,y):
        super().__init__(img_path,x,y)
        self.is_hited = False  # 记录是否被击中
        self.bullets = []#记录子弹

    def is_rate(self):
        if self.is_hited:
            self.img = pygame.image.load("../img/hero_blowup_n3.png")


    def move_lift(self):
        if self.x >= 0:
            self.x -= 8
            self.is_rate()
    def move_right(self):
        if self.x <= WINDOW_WIDTH-60:
            self.x += 8
            self.is_rate()
    def move_up(self):
        if self.y >= 0:
            self.y -= 8
            self.is_rate()
    def move_down(self):
        if self.y <= WINDOW_HEIGHT-80:
            self.y += 8
            self.is_rate()
    def fire(self):
        """发射子弹"""
        buttle = Bullet("../img/bullet.png",self.x+29,self.y-22)
        buttle.display()
        #将子弹添加到列表中
        self.bullets.append(buttle)
    def display_bullet(self):
        """贴子弹"""
        delete_bullets = []
        for bullet in self.bullets:
            if bullet.y >= 0:
                #判断是否击中飞机
                for enemy in enemy_list:
                    if bullet.is_hit_plane(enemy): #击中某架飞机
                        #记录要删除的子弹
                        delete_bullets.append(bullet)
                        #让敌机记录被击中的状态
                        enemy.is_hited = True
                        global score
                        score += 10
                        break
                    else:
                        bullet.display()
                        bullet.move()
            else:
                delete_bullets.append(bullet)

        for out_window_bullet in delete_bullets:
            self.bullets.remove(out_window_bullet)

def main():#主函数
    # #初始化pygame库,让计算机准备
    pygame.init()
    #1.创建窗口
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    Item.window = window
    #贴背景图
    #加载图片文件，返回图片对象
    map = Map("../img/background_2.jpg",0,0)
    # bg_img = pygame.image.load("../img/backtp.png")
    #创建飞机对象
    hero_plane = HeroPlane("../img/plane802.png",200,700)
    plane_list.append(hero_plane)


    enemy_plane = EnemyPlane("../img/enemy2.png" ,180,0)
    enemy_list.append(enemy_plane)

    #加载自定义字体，返回字体对象
    font_obj = pygame.font.Font("../img/ziti.TTF",30)

    while True:
        #贴图
        map.display()

        #贴敌机图

        enemy_plane.display()
        enemy_plane.fire()
        enemy_plane.display_bullet()
        enemy_plane.move()

            # 飞机贴图
        hero_plane.display()
        # 贴子弹图
        hero_plane.display_bullet()
        # 设置文本返回文本对象
        text_obj = font_obj.render("得分：%d" % score, 1, (255, 255, 255))
        # 贴文本
        window.blit(text_obj,(10,10))
        map.map_move()
        #暂停
        background = pygame.image.load("../img/stop2.png")
        window.blit(background, (400,20))
        #返回
        background = pygame.image.load("../img/return.png")
        window.blit(background, (20,20))
        #刷新窗口
        pygame.display.update()
        x, y = pygame.mouse.get_pos()
        # print(x,y)
        # 获取事件，比如按键等
        for event in pygame.event.get():

            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # print(event.key)
                # 检测按键是否是空格键
                if event.key == K_SPACE:
                    print('space')
                    hero_plane.fire()
                if event.key == K_ESCAPE :
                    Mmain.main()
                if event.key == K_BACKSPACE:
                    background = pygame.image.load("../img/start3.png")
                    window.blit(background, (120,250))
                    print('1')
                     #刷新窗口
                    pygame.display.update()
                    #写判断点击改变item_s
                    item = True
                    while item:
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                print('anjia')
                                if event.key == K_BACKSPACE:
                                    item = not item
                                    print('qujian')
                    #刷新窗口
                    pygame.display.update()

            elif event.type == MOUSEBUTTONDOWN:
                if 400 <= x <= 480 and 20 <= y <= 48:
                    background = pygame.image.load("../img/start3.png")
                    window.blit(background, (120,250))
                    print('1')
                     #刷新窗口
                    pygame.display.update()
                    #写判断点击改变item_s
                    item = True
                    while item:
                        x, y = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONDOWN:
                                print('anjia')
                                print(x,y)
                                if 117 <= x <= 360 and 248 <= y <= 488:
                                    item = not item
                                    print('qujian')
                    #刷新窗口
                    pygame.display.update()
                if  20<= x <= 50 and 20 <= y <= 50:
                    Mmain.main()
        # 获取当键盘的长按事件
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            print("left")
            hero_plane.move_lift()
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            print("right")
            hero_plane.move_right()
        if pressed_keys[K_w] or pressed_keys[K_UP]:
            hero_plane.move_up()
        if pressed_keys[K_s] or pressed_keys[K_DOWN]:
            hero_plane.move_down()

        time.sleep(0.02)

if __name__ == '__main__':
    main()

