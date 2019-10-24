# -*- coding:utf-8 -*-
import pygame
import time
import random
from pygame.locals import *
import sys

WINDOW_WIDTH = 480  # 窗口宽
WINDOW_HEIGHT = 700 #窗口高
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

    def move(self):
        """向下移"""
        self.y += 3
        #判断是否飞出边界
        if self.y >=WINDOW_HEIGHT or self.is_hited:
            #如果飞出则重新设置飞机位置
            self.img = pygame.image.load("../img/hero_blowup_n4.png")

            self.y = random.randint(-200,0)
            self.x = random.randint(0,WINDOW_WIDTH-60)
            #换一个飞机出场
            self.img = pygame.image.load("../img/plane_%d.png" % random.randint(1,4))
            #还原状态
            if self.is_hited:
                self.is_hited = False
    #敌机开火
    def fire(self):
        random_num = random.randint(1, 50)
        if random_num == 8:
            bullet = Bullet("../img/bullet-1.gif",self.x+35,self.y+50)
            bullet.display()
            #添加子弹
            self.bullets.append(bullet)

    def display_bullet(self):
        # for bullet in self.bullets:
        #     bullet.display()
        #     bullet.move_bullet()
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
    hero_plane = HeroPlane("../img/plane802.png",200,550)
    plane_list.append(hero_plane)

    for _ in range(ENEMY_COUNT):
        enemy_plane = EnemyPlane("../img/plane_%d.png" % random.randint(1,4),random.randint(0,WINDOW_WIDTH-80),random.randint(-300,0))
        enemy_list.append(enemy_plane)

    #加载自定义字体，返回字体对象
    font_obj = pygame.font.Font("../img/ziti.TTF",30)

    while True:
        #贴图
        map.display()
        #飞机贴图
        hero_plane.display()
        #贴子弹图
        hero_plane.display_bullet()
        #贴敌机图
        for enemy in enemy_list:
            enemy.display()
            enemy.fire()
            enemy.display_bullet()
            enemy.move()

        # 设置文本返回文本对象
        text_obj = font_obj.render("得分：%d" % score, 1, (255, 255, 255))
        # 贴文本
        window.blit(text_obj,(10,10))
        map.map_move()
        #刷新窗口
        pygame.display.update()

        # 获取事件，比如按键等
        for event in pygame.event.get():
            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是空格键
                if event.key == K_SPACE:
                    print('space')
                    hero_plane.fire()

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
