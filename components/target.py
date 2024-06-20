import pygame as pg
import os
import config

base_dir = os.path.dirname(os.path.dirname(__file__))  # 从components目录回到主目录
target_path = os.path.join(base_dir, 'static', 'img', 'target.png')

class Target(pg.sprite.Sprite):
    def __init__(self, target_center_x, target_center_y):
        super().__init__()
        self.width = config.TARGET_WIDTH
        self.height = config.TARGET_HEIGHT

        self.image_src = pg.image.load(target_path).convert()
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (target_center_x, target_center_y)  # 中心坐标 ****

        self.scale = 1
        self.scale_delta = 0.01

    def update(self):
        self.scale += self.scale_delta
        if self.scale > 1.1 or self.scale < 0.9:
            self.scale_delta *= -1
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.image = pg.transform.scale(self.image_src, (self.width * self.scale, self.height * self.scale))