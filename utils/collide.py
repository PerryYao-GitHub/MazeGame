import pygame as pg

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

def collide_circle():
    pass