import pygame as pg

def draw_text(screen, text, size, x, y):
    font = pg.font.SysFont('Arial', size)
    image = font.render(text, True, "white")
    rect = image.get_rect()
    rect.center = (x, y)
    screen.blit(image, rect)