# 创建GameManager来管理游戏对象
import pygame as pg
from player import Player
from wall import Wall
from utils.collide import collide_rect

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.player = None
        self.walls = pg.sprite.Group()
        # wall = Wall(200, 200, 500, 50)
        # wall.add(self.walls)
        self.load()

    def load_player(self, player_center_x, player_center_y, player_angle):
        if self.player: self.player.kill()  # 把之前的 player 清空, 避免阻塞; 一定要写 if 因为 'NoneType' object has no attribute 'kill'
        self.player = Player(player_center_x, player_center_y, player_angle)

    def load_walls(self, walls_info):
        self.walls.empty()
        for (wall_x, wall_y, wall_width, wall_height) in walls_info:
            wall = Wall(wall_x, wall_y, wall_width, wall_height)
            wall.add(self.walls)

    def load(self):
        with open("static/level/level_1.txt") as fin:
            player_center_x, player_center_y, player_angle = map(int, fin.readline().split())
            self.load_player(player_center_x, player_center_y, player_angle)

            walls_cnt = int(fin.readline())
            walls_info = []
            for _ in range(walls_cnt):
                walls_info.append(map(int, fin.readline().split()))
            self.load_walls(walls_info)

    def check_collide(self):
        if pg.sprite.spritecollide(self.player, self.walls, False, collide_rect):  # 返回一个列表, 展示与哪些墙碰撞了
            self.player.crash()

    def update(self):
        self.player.update()
        self.check_collide()
        self.screen.blit(self.player.image, self.player.rect)
        self.walls.update()  # 继承至父类
        self.walls.draw(self.screen)  # 继承至父类