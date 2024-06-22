import pygame as pg
import config
from game_manager import GameManager
from utils.draw import draw_text

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pg.time.Clock()

pg.mixer.music.load("static/audio/bgm.wav")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)  # 参数 -1 表示循环播放bgm

# player = Player()  等价于
game_manager = GameManager(screen)

running = True
while running:
    # 退出机制
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        elif not game_manager.level_exists and event.type == pg.KEYDOWN: running = False

    # 画图

    if not game_manager.level_exists:
        screen.fill("black")  # 画背景
        draw_text(screen, "Win!", 200, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
        pg.display.flip()
    else:
        screen.fill("black")  # 画背景
        game_manager.update()
        pg.display.flip()

    # 帧率
    clock.tick(config.FPS)  # 一秒钟将上面的死循环执行 60 次

pg.quit()