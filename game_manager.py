# 创建GameManager来管理游戏对象
import pygame as pg
from player import Player
from wall import Wall

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.walls = pg.sprite.Group()
        wall = Wall(200, 200, 500, 50)
        wall.add(self.walls)

    def check_collide(self):
        if pg.sprite.spritecollide(self.player, self.walls, False):  # 返回一个列表, 展示与哪些墙碰撞了
            self.player.crash()

    def update(self):
        self.player.update()
        self.check_collide()
        self.screen.blit(self.player.image, self.player.rect)
        self.walls.update()  # 继承至父类
        self.walls.draw(self.screen)  # 继承至父类