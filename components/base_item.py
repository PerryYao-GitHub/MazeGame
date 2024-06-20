import pygame as pg
import os

import config

base_dir = os.path.dirname(os.path.dirname(__file__))  # 从components目录回到主目录
star_path = os.path.join(base_dir, 'static', 'img', 'star.png')
target_path = os.path.join(base_dir, 'static', 'img', 'target.png')

class BaseItem(pg.sprite.Sprite):
    def __init__(self, image_path, center_x, center_y, width, height):
        super().__init__()
        self.width, self.height = width, height

        self.image_src = pg.image.load(image_path).convert()
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)

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



class Star(BaseItem):
    def __init__(self, star_center_x, star_center_y):
        super().__init__(image_path=star_path, center_x=star_center_x, center_y=star_center_y, width=config.STAR_WIDTH, height=config.STAR_HEIGHT)  # super().__init__() 中不能写 self

class Target(BaseItem):
    def __init__(self, target_center_x, target_center_y):
        super().__init__(image_path=target_path, center_x=target_center_x, center_y=target_center_y, width=config.TARGET_WIDTH, height=config.TARGET_HEIGHT)
