import pygame as pg
import math
import config

def collide_rect(player, wall):
    coordinates = []
    for (i, j) in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        offset = pg.Vector2(i * player.width / 2 * 0.8, j * player.height / 2 * 0.8).rotate(player.angle)
        coordinates.append(offset + player.rect.center)

    points_cnt = len(coordinates)
    for i in range(points_cnt):
        point1 = coordinates[i]
        point2 = coordinates[(i + 1) % points_cnt]
        if wall.rect.clipline(point1, point2): return True
    return False

def collide_circle(player, star):
    player_x, player_y = player.rect.center
    star_x, star_y = star.rect.center
    dis = math.sqrt((player_x - star_x) ** 2 + (player_y - star_y) ** 2)
    if dis < config.STAR_WIDTH: return True
    return False