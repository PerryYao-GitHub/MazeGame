# 创建GameManager来管理游戏对象
import pygame as pg
import os

from components.player import Player
from components.wall import Wall
from components.base_item import Star
from components.base_item import Target
from utils.collide import collide_rect, collide_circle

class GameManager:
    def __init__(self, screen):
        """定义游戏中所有的 components"""
        self.screen = screen

        self.player = None

        self.walls = pg.sprite.Group()

        self.stars = pg.sprite.Group()
        self.stars_cnt = 0  # 将星星维护起来
        self.eat_starts_audio = pg.mixer.Sound("static/audio/eat_stars.wav")
        self.eat_starts_audio.set_volume(0.2)

        self.targets_cnt = 0
        self.targets = pg.sprite.Group()
        self.success_audio = pg.mixer.Sound("static/audio/success.wav")
        self.success_audio.set_volume(0.2)
        self.has_success = False
        self.success_time = -1
        self.level_exists = True  # 当前关卡是否存在
        self.level = 1  # 关卡数

        # 加载以上 components
        self.load()

    def load_player(self, player_x, player_y, player_angle):
        if self.player: self.player.kill()  # 把之前的 player 清空, 避免阻塞; 一定要写 if 因为 'NoneType' object has no attribute 'kill'
        self.player = Player(player_x, player_y, player_angle)

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

    def load_targets(self, targets_info):
        self.targets.empty()
        for (target_x, target_y) in targets_info:
            target = Target(target_x, target_y)
            target.add(self.targets)

    def load(self):
        self.success_time = -1  # load 新关卡, 重置获胜时刻
        self.has_success = False  # load 新的关卡, 重置当前获胜状态
        if not os.path.isfile("static/level/level_{}.txt".format(self.level)):
            self.level_exists = False  # 如果没有当前关卡, level_exists = False
            return 0

        with open("static/level/level_{}.txt".format(self.level)) as fin:
            # 先 load player 信息
            player_center_x, player_center_y, player_angle = map(int, fin.readline().split())
            self.load_player(player_center_x, player_center_y, player_angle)

            # load 墙信息
            walls_cnt = int(fin.readline())
            walls_info = []
            for _ in range(walls_cnt):
                walls_info.append(map(int, fin.readline().split()))
            self.load_walls(walls_info)

            # load 星星信息
            self.stars_cnt = int(fin.readline())
            stars_info = []
            for _ in range(self.stars_cnt):
                stars_info.append(map(int, fin.readline().split()))
            self.load_stars(stars_info)

            self.targets_cnt = int(fin.readline())
            target_info = []
            for _ in range(self.targets_cnt):
                target_info.append(map(int, fin.readline().split()))
            self.load_targets(target_info)

    def check_collide(self):
        if pg.sprite.spritecollide(self.player, self.walls, False, collide_rect):  # 返回一个列表, 展示与哪些墙碰撞了
            self.player.crash()
        if pg.sprite.spritecollide(self.player, self.stars, True, collide_circle):
            self.stars_cnt -= 1
            self.eat_starts_audio.play()

        if self.stars_cnt == 0 and pg.sprite.spritecollide(self.player, self.targets, True, collide_circle):
            self.success_audio.play()
            self.has_success = True

    def update(self):
        # update star
        self.stars.update()
        self.stars.draw(self.screen)

        # update player
        self.player.update()
        self.check_collide()

        # update walls
        self.walls.update()  # 继承至父类
        self.walls.draw(self.screen)  # 继承至父类

        # update targets
        self.targets.update()
        self.targets.draw(self.screen)

        # update 屏幕
        self.screen.blit(self.player.image, self.player.rect)

        if self.has_success:
            if self.success_time < 0:  # 如果是刚刚成功，记录时间
                self.success_time = pg.time.get_ticks()
            elif pg.time.get_ticks() - self.success_time > 4000:  # 检查是否已经过了足够的时间 (例如 4000 毫秒)
                    self.level += 1
                    self.load()




