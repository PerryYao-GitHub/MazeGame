import pygame as pg

class Wall(pg.sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.image = pg.Surface((wall_width, wall_height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y