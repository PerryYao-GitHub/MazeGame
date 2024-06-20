import pygame as pg
import os
import config

base_dir = os.path.dirname(os.path.dirname(__file__))  # 从components目录回到主目录
star_path = os.path.join(base_dir, 'static', 'img', 'star.png')

class Star(pg.sprite.Sprite):
    def __init__(self, star_center_x, star_center_y):
        super().__init__()
        self.width = config.STAR_WIDTH
        self.height = config.STAR_HEIGHT

        self.image_src = pg.image.load(star_path).convert()
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (star_center_x, star_center_y)  # 中心坐标 ****

    def update(self):
        pass