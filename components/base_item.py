import pygame as pg

class BaseItem(pg.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
