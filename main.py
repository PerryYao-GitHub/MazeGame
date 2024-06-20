import pygame as pg
import config
from game_manager import GameManager

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()

# player = Player()  等价于
game_manager = GameManager(screen)

running = True
while running:
    # 退出机制
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # 画图
    screen.fill("black")  # 画背景
    # screen.blit(player.image, player.rect)  # 画小车
    # player.update()
    # 等价于
    game_manager.update()


    pg.display.flip()

    # 帧率
    clock.tick(config.FPS)  # 一秒钟将上面的死循环执行 60 次

pg.quit()