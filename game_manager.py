# 创建GameManager来管理游戏对象
import pygame as pg

from components.star import Star
from utils.collide import collide_rect

from components.player import Player
from components.wall import Wall

class GameManager:
    def __init__(self, screen):
        """定义游戏中所有的 components"""
        self.screen = screen
        self.player = None
        self.walls = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.targets = pg.sprite.Group()

        # 加载以上 components
        self.load()

    def load_player(self, player_center_x, player_center_y, player_angle):
        if self.player: self.player.kill()  # 把之前的 player 清空, 避免阻塞; 一定要写 if 因为 'NoneType' object has no attribute 'kill'
        self.player = Player(player_center_x, player_center_y, player_angle)

    def load_walls(self, walls_info):
        self.walls.empty()
        for (wall_x, wall_y, wall_width, wall_height) in walls_info:
            wall = Wall(wall_x, wall_y, wall_width, wall_height)
            wall.add(self.walls)

    def load_stars(self, stars_info):
        self.stars.empty()
        for (start_x, start_y) in stars_info:
            star = Star(start_x, start_y)
            star.add(self.stars)

    def load(self):
        with open("static/level/level_1.txt") as fin:
            player_center_x, player_center_y, player_angle = map(int, fin.readline().split())
            self.load_player(player_center_x, player_center_y, player_angle)

            walls_cnt = int(fin.readline())
            walls_info = []
            for _ in range(walls_cnt):
                walls_info.append(map(int, fin.readline().split()))
            self.load_walls(walls_info)

            stars_cnt = int(fin.readline())
            stars_info = []
            for _ in range(stars_cnt):
                stars_info.append(map(int, fin.readline().split()))
            self.load_stars(stars_info)

    def check_collide(self):
        if pg.sprite.spritecollide(self.player, self.walls, False, collide_rect):  # 返回一个列表, 展示与哪些墙碰撞了
            self.player.crash()

    def update(self):
        # update player
        self.player.update()
        self.check_collide()

        # update 屏幕
        self.screen.blit(self.player.image, self.player.rect)

        # update walls
        self.walls.update()  # 继承至父类
        self.walls.draw(self.screen)  # 继承至父类

        # update star
        self.stars.update()
        self.stars.draw(self.screen)