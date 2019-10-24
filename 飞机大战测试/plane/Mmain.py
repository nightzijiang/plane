import pygame

import jingdian as mold1

import Boss as mole2

from pygame.locals import *
from sys import exit


def main():
    # def Mmain():
    pygame.init()
    screen = pygame.display.set_mode((480,852),0,32)
    background = pygame.image.load("../img/Mbj.jpg")
    # mouse_cursor = pygame.image.load('feiji/plane.png')
    #设置窗口标题
    pygame.display.set_caption('飞机大战')
    #创建按钮区域


    while 1 :
        #加入背景图
        screen.blit(background,(0,0))
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE :
                    exit()
                if event.key == K_1:
                    mold1.main()
            if event.type == MOUSEBUTTONDOWN:
                if 116 <= x <= 370 and 409 <= y <= 475:
                    mold1.main()                                  #1
            #109 360  560 620
                elif 109 <= x <= 360 and 560 <= y <= 620:
                    mole2.main()                                  #2
            #44 190 732 785     254 436  733 785
                elif 44 <= x <= 190 and 732 <= y <= 785:
                    backgrounds = pygame.image.load("../img/option.png")
                    screen.blit(backgrounds, (50,250))
                    print('1')
                     #刷新窗口
                    pygame.display.update()
                    #写判断点击改变item_s
                    item = True
                    while item:
                        x, y = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == KEYDOWN:
                                if event.key == K_ESCAPE :
                                    main()

                            if event.type == MOUSEBUTTONDOWN:
                                print('anjia')
                                print(x,y)
                                if 389 <= x <= 413 and 264 <= y <= 290:
                                    item = not item
                                    print('qujian')
                                    
                    #刷新窗口
                    pygame.display.update()
                elif 254 <= x <= 436 and 733 <= y <= 785:
                    exit()
        #加入背景图
        screen.blit(background,(0,0))
        #刷新画面
        pygame.display.update()



if __name__ == '__main__':
    main()

